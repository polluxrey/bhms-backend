from rest_framework import status, generics, exceptions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from payment.models import Payment, PaymentType, PaymentMethod
from payment.serializers import PaymentSerializer, PaymentListSerializer, PaymentTypeSerializer, PaymentMethodSerializer
from payment.pagination import PaymentPagination
from bhms.utils import send_email, send_sms
from django.conf import settings
from users.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging
from django.template.loader import render_to_string
from rest_framework.generics import RetrieveAPIView

# Create your views here.
# views.py


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(
            data=request.data,
            fields=["boarder", "payment_type", "payment_method",
                    "amount", "description", "receipt"]
        )

        if serializer.is_valid():
            instance = serializer.save()

            context = {
                "first_name": instance.boarder.first_name,
                "full_name": instance.boarder.full_name,
                "payment_type": instance.payment_type.name,
                "payment_method": instance.payment_method.name,
                "amount": instance.amount,
                "description": instance.description,
            }

            send_email(
                subject="Your Payment Has Been Submitted",
                to=[instance.boarder.email],
                template_name="emails/payment_submitted.txt",
                context=context,
                from_email=settings.EMAIL_HOST_USER,
            )

            owners = User.objects.filter(groups__name="Owner")

            for owner in owners:
                send_email(
                    subject="New Payment Submitted",
                    to=[owner.email],
                    template_name="emails/new_payment_notification.txt",
                    context={**context, "owner_first_name": owner.first_name},
                    from_email=settings.EMAIL_HOST_USER,
                )

            return Response({'message': 'Data saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListCreateView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = PaymentPagination

    def get_queryset(self):
        boarder_id = self.request.query_params.get("boarderId")
        if not boarder_id:
            raise exceptions.ValidationError(
                {"detail": "boarderId query parameter is required."}
            )

        return Payment.objects.filter(boarder=boarder_id).order_by("-created_at")

    def get_serializer(self, *args, **kwargs):
        """
        Override to pass dynamic fields to the serializer
        """
        kwargs["fields"] = ["boarder",
                            "created_at_date_display", "amount", "status"]
        return super().get_serializer(*args, **kwargs)


class ActivePaymentTypeListView(ReadOnlyModelViewSet):
    queryset = PaymentType.objects.filter(is_active=True)
    serializer_class = PaymentTypeSerializer


class ActivePaymentMethodListView(ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer


class BoarderPaymentsListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = PaymentPagination

    def get_queryset(self):
        boarder_id = self.request.query_params.get("boarder_id")
        if not boarder_id:
            raise exceptions.ValidationError(
                {"detail": "boarder_id query parameter is required."}
            )

        return Payment.objects.filter(boarder=boarder_id).order_by("-created_at")

    def get_serializer(self, *args, **kwargs):
        """
        Override to pass dynamic fields to the serializer
        """
        kwargs["fields"] = [
            "id",
            "created_at_date_display",
            "payment_type_name",
            "payment_method_name",
            "amount",
            "status",
        ]
        return super().get_serializer(*args, **kwargs)


class UpdatePaymentStatusView(APIView):
    VALID_ACTIONS = {
        "confirm": "CONFIRMED",
        "refund": "REFUNDED",
    }

    def post(self, request):
        payment_id = request.data.get("id")
        action = request.data.get("action")

        if not payment_id or not action:
            return Response(
                {"error": "Missing required query parameter/s."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        action = action.lower()
        if action not in self.VALID_ACTIONS:
            return Response(
                {"error": "Invalid action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.filter(pk=payment_id).first()
        if not payment:
            return Response(
                {"error": f"Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = self.VALID_ACTIONS[action]
        payment.status = new_status
        payment.save(update_fields=["status"])

        boarder = payment.boarder
        phone_number = getattr(boarder, "phone_number", None)
        email = getattr(boarder, "email", None)

        sent = False

        if not phone_number:
            context = {
                "amount": payment.amount,
                "payment_type_name": payment.payment_type.name,
                "status": payment.get_status_display(),
            }

            message = render_to_string(
                "sms/payment_status_update.txt", context).strip()

            try:
                response = send_sms(phone_number, message)
                if response and response.get("status") == 200:
                    sent = True
            except Exception as e:
                logging.error(f"Failed to send SMS to {phone_number}: {e}")

        if not sent and email:
            context = {
                "first_name": boarder.first_name,
                "amount": payment.amount,
                "payment_type_name": payment.payment_type.name,
                "payment_method_name": payment.payment_method.name,
                "status": payment.get_status_display().upper(),
                "date": payment.created_at.strftime("%B %d, %Y %I:%M %p")
            }

            try:
                send_email(
                    subject=f"Your Payment Has Been {payment.get_status_display()}",
                    to=[boarder.email],
                    template_name="emails/payment_status_update.txt",
                    context=context,
                    from_email=settings.EMAIL_HOST_USER,
                )
            except Exception as e:
                logging.error(f"Failed to send email to {email}: {e}")
        else:
            pass

        return Response(
            {"message": f"Payment has been {new_status.lower()}."},
            status=status.HTTP_200_OK,
        )


class PaymentDetailView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Override to pass dynamic fields to the serializer
        """
        kwargs["fields"] = [
            "id",
            "boarder_full_name",
            "created_at_datetime_display",
            "payment_type_name",
            "payment_method_name",
            "amount",
            "status",
            "description",
            "receipt"
        ]
        return super().get_serializer(*args, **kwargs)
