import logging
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from service_request.models import ServiceRequest
from service_request.serializers import ServiceRequestCreateSerializer, ServiceRequestDetailSerializer, ServiceRequestTypeSerializer, ServiceRequestListSerializer
from boarder.models import Boarder
from bhms.utils import send_email
from bhms.choices import RequestType, RequestStatus
from django.conf import settings
from users.models import User
from service_request.pagination import ServiceRequestPagination
from django.db.models import Value, F
from django.db.models.functions import Concat


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

            try:
                send_email(
                    subject="Your Request Has Been Submitted",
                    to=[instance.boarder.email],
                    template_name="emails/request_submitted.txt",
                    context=context,
                    from_email=settings.EMAIL_HOST_USER,
                )
            except Exception as e:
                logging.error(
                    f"Failed to send email to {instance.boarder.email}: {e}")

            owners = User.objects.filter(groups__name="Owner")

            for owner in owners:
                try:
                    send_email(
                        subject="New Request Submitted",
                        to=[owner.email],
                        template_name="emails/new_request_notification.txt",
                        context={**context,
                                 "owner_first_name": owner.first_name},
                        from_email=settings.EMAIL_HOST_USER,
                    )
                except Exception as e:
                    logging.error(
                        f"Failed to send email to {owner.email}: {e}")

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


class RequestStatusAPIView(APIView):
    def get(self, request):
        data = [
            {"value": choice[0], "label": choice[1]}
            for choice in RequestStatus.choices
        ]
        return Response(data)


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all().order_by("-created_at")
    pagination_class = ServiceRequestPagination

    SORT_MAP = {
        "ref_no": "reference_number",
        "boarder": "boarder_full_name",
        "type": "request_type",
        "date": "created_at",
    }

    def get_serializer_class(self):
        if self.action == "list":
            view = self.request.query_params.get("view")
            if view == "detailed":
                return ServiceRequestDetailSerializer
            return ServiceRequestListSerializer

        return ServiceRequestDetailSerializer

    def get_queryset(self):
        if self.action == "list":
            queryset = super().get_queryset()

            params = self.request.query_params

            boarder = params.get("boarder")
            request_type = params.get("type")
            reference_number = params.get("ref_no")
            active = params.get("active")
            sort_key = params.get("sort")
            sort_direction = params.get("dir")

            if boarder:
                queryset = queryset.filter(boarder_id=boarder.strip())

            if request_type:
                queryset = queryset.filter(
                    request_type__iexact=request_type.strip()
                )

            if reference_number:
                queryset = queryset.filter(
                    reference_number__iexact=reference_number.strip()
                )

            if active and active.lower() == "true":
                queryset = queryset.filter(
                    status__in=[
                        RequestStatus.PENDING,
                        RequestStatus.IN_PROGRESS
                    ]
                )

            # For full name
            queryset = queryset.annotate(
                boarder_full_name=Concat(
                    F("boarder__last_name"),
                    Value(", "),
                    F("boarder__first_name"),
                    Value(" "),
                    F("boarder__middle_name"),
                )
            )

            if sort_key:
                sort_key = sort_key.strip().lower()
                sort_key = self.SORT_MAP.get(sort_key, sort_key)
                if sort_direction and sort_direction.lower() == "desc":
                    sort_key = f"-{sort_key}"
                queryset = queryset.order_by(sort_key)

            return queryset

        return super().get_queryset()

    @action(detail=False, methods=["patch"])
    def update_status_by_ref(self, request):
        reference_number = request.data.get("ref_no")
        new_status = request.data.get("status")
        admin_remarks = request.data.get("remarks")

        if not reference_number:
            return Response(
                {"error": "Reference number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not new_status and admin_remarks is None:
            return Response(
                {"error": "Either request status or admin remarks is required"},
                status=400
            )

        try:
            service_request = ServiceRequest.objects.get(
                reference_number=reference_number)
        except ServiceRequest.DoesNotExist:
            return Response(
                {"error": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if service_request.status in ["RESOLVED", "REJECTED"]:
            return Response(
                {"error": f"This request has already been {service_request.get_status_display().lower()} and cannot be edited"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if (
            new_status == service_request.status and
            admin_remarks == service_request.admin_remarks
        ):
            return Response(
                {"message": "No changes detected"},
                status=status.HTTP_200_OK
            )

        if new_status:
            if new_status not in RequestStatus.values:
                return Response(
                    {"error": "Invalid status"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            service_request.status = new_status

        if admin_remarks is not None:
            service_request.admin_remarks = admin_remarks

        service_request.save()

        return Response(
            {
                "message": "Status updated successfully"
            },
            status=status.HTTP_200_OK
        )
