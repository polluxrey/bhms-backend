# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from otp.models import OTP
from boarder.models import Boarder
from otp.serializers import SendOTPSerializer, VerifyOTPSerializer
from otp.utils import generate_otp, mask_email
from bhms.utils import send_sms_semaphore
from django.utils import timezone
from django.db import transaction
from datetime import timedelta


class SendOTPAPIView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        boarder_id = serializer.validated_data['boarder_id']

        try:
            boarder = Boarder.objects.get(id=boarder_id)
        except Boarder.DoesNotExist:
            return Response({'error': 'Invalid boarder ID'}, status=status.HTTP_404_NOT_FOUND)

        if not boarder.email:
            return Response(
                {'error': 'No email address found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_code = generate_otp()
        OTP.objects.create(boarder=boarder, code=otp_code)

        # Send OTP to the user's email
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is {otp_code}',
            from_email=None,
            recipient_list=[boarder.email],
            fail_silently=False,
        )

        masked_email = mask_email(boarder.email)

        return Response(
            data={
                'message': 'OTP sent to your registered email.',
                'masked_email': masked_email
            },
            status=status.HTTP_200_OK
        )


class SendOTPAPIView_v2(APIView):
    OTP_RATE_LIMITS = {
        # SMS-specific limit
        'sms': {'max_requests': 5, 'window_minutes': 60},
        # Email-specific limit
        'email': {'max_requests': 5, 'window_minutes': 30},
    }

    def is_rate_limited(self, boarder, channel):
        limit = self.OTP_RATE_LIMITS.get(
            channel,
            {'max_requests': 5, 'window_minutes': 60}
        )

        recent_count = OTP.objects.filter(
            boarder=boarder,
            channel=channel,
            created_at__gte=timezone.now(
            ) - timedelta(minutes=limit['window_minutes'])
        ).count()

        return recent_count >= limit['max_requests']

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        boarder_id = serializer.validated_data['boarder_id']

        try:
            boarder = Boarder.objects.get(id=boarder_id)
        except Boarder.DoesNotExist:
            return Response(
                {'error': 'Boarder not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        otp_code = generate_otp()

        with transaction.atomic():
            # Invalidate previous OTPs
            OTP.objects.filter(
                boarder=boarder,
                is_active=True,
            ).update(is_active=False)

            # if boarder.phone_number:
            #     if self.is_rate_limited(boarder, 'sms'):
            #         return Response(
            #             {'error': 'Too many OTP requests via SMS. Try again later.'},
            #             status=status.HTTP_429_TOO_MANY_REQUESTS
            #         )

            #     sms_response = send_sms_semaphore(
            #         message=f'Your OTP is {otp_code}',
            #         phone_number=boarder.phone_number
            #     )

            #     if sms_response and sms_response[0].get("status") in ["Sent", "Pending"]:
            #         OTP.objects.create(
            #             boarder=boarder,
            #             code=otp_code,
            #             channel=OTP.Channel.SMS,
            #         )

            #         return Response(
            #             data={
            #                 'otp_channel': OTP.Channel.SMS,
            #                 'status': 'otp_sent',
            #                 'phone_suffix': boarder.phone_number[-3:]
            #             },
            #             status=status.HTTP_200_OK
            #         )

            if boarder.email:
                if self.is_rate_limited(boarder, 'email'):
                    return Response(
                        {'error': 'Too many OTP requests via email. Try again later.'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )

                sent_count = send_mail(
                    subject='OTP Code',
                    message=f'Your OTP is {otp_code}',
                    from_email=None,
                    recipient_list=[boarder.email],
                    fail_silently=True,
                )

                if sent_count == 1:
                    OTP.objects.create(
                        boarder=boarder,
                        code=otp_code,
                        channel=OTP.Channel.EMAIL,
                    )

                    masked_email = mask_email(boarder.email)

                    return Response(
                        data={
                            'otp_channel': OTP.Channel.EMAIL,
                            'status': 'otp_sent',                            'masked_email': masked_email
                        },
                        status=status.HTTP_200_OK
                    )

        return Response(
            {'message': 'Failed to send OTP.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        boarder_id = serializer.validated_data['boarder_id']
        otp_code = serializer.validated_data['otp']

        try:
            boarder = Boarder.objects.get(id=boarder_id)
        except Boarder.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            otp = OTP.objects.select_for_update().filter(
                boarder=boarder,
                code=otp_code,
                is_verified=False
            ).order_by('-created_at').first()

            if not otp or otp.is_expired:
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

            otp.is_verified = True
            otp.save(update_fields=['is_verified'])

        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
