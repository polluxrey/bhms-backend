# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from otp.models import OTP
from boarder.models import Boarder
from otp.serializers import SendOTPSerializer, VerifyOTPSerializer
from otp.utils import generate_otp, mask_email


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


class VerifyOTPAPIView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        boarder_id = serializer.validated_data['boarder_id']
        otp_code = serializer.validated_data['otp']

        try:
            boarder = Boarder.objects.get(id=boarder_id)
        except Boarder.DoesNotExist:
            return Response({'error': 'Invalid boarder ID'}, status=status.HTTP_404_NOT_FOUND)

        otp = OTP.objects.filter(
            boarder=boarder,
            code=otp_code
        ).order_by('-created_at').first()

        if otp is None:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired() or otp.is_verified:
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        otp.is_verified = True
        otp.save()

        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
