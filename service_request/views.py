from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from service_request.models import ServiceRequest
from service_request.serializers import ServiceRequestCreateSerializer, ServiceRequestDetailSerializer, ServiceRequestTypeSerializer
from boarder.models import Boarder
from bhms.utils import send_email
from bhms.choices import RequestType
from django.conf import settings
from users.models import User


class ServiceRequestView(APIView):
    def post(self, request):
        serializer = ServiceRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            context = {
                "first_name": instance.boarder.first_name,
                "full_name": instance.boarder.full_name,
                "reference_number": instance.reference_number,
                "request_type": instance.get_request_type_display(),
                "description": instance.description,
            }

            send_email(
                subject="Your Request Has Been Submitted",
                to=[instance.boarder.email],
                template_name="emails/request_submitted.txt",
                context=context,
                from_email=settings.EMAIL_HOST_USER,
            )

            owners = User.objects.filter(groups__name="Owner")

            for owner in owners:
                send_email(
                    subject="New Request Submitted",
                    to=[owner.email],
                    template_name="emails/new_request_notification.txt",
                    context={**context, "owner_first_name": owner.first_name},
                    from_email=settings.EMAIL_HOST_USER,
                )

            return Response(
                {
                    "message": "Request created successfully!",
                    "reference_number": instance.reference_number,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceRequestLookupView(APIView):
    def get(self, request):
        ref = request.query_params.get('ref')
        if not ref:
            return Response(
                {'error': 'Reference number is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service_request = ServiceRequest.objects.get(reference_number=ref)
        except ServiceRequest.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceRequestDetailSerializer(
            service_request, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceRequestTypeChoicesView(APIView):
    def get(self, request):
        choices_data = [
            {'value': choice_value, 'label': choice_label}
            for choice_value, choice_label in RequestType.choices
        ]
        serializer = ServiceRequestTypeSerializer(choices_data, many=True)
        return Response(serializer.data)
