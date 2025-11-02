from django.db.models import F, Q, Case, When, Value, IntegerField
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from boarder.models import Boarder
from boarder.serializers import (
    BoarderNameSerializer, BoarderListSerializer, BoarderDisplaySerializer, BoarderDetailSerializer, BoarderPaymentsSerializer)
from boarder.pagination import BoarderListPagination
from django.db.models import OuterRef, Subquery, DateTimeField
from payment.models import Payment


class ActiveBoarderNameListView(viewsets.ReadOnlyModelViewSet):
    queryset = Boarder.objects.filter(is_active=True).order_by(
        "last_name", "first_name", "middle_name")
    serializer_class = BoarderNameSerializer


class BoarderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Boarder.objects.all().order_by(
        '-is_active', 'last_name', 'first_name', 'middle_name')
    pagination_class = BoarderListPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return BoarderListSerializer
        elif self.action == 'retrieve':
            return BoarderDisplaySerializer
        return BoarderDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        last_name = self.request.query_params.get('last_name')
        first_name = self.request.query_params.get('first_name')
        is_active = self.request.query_params.get('is_active')

        if last_name:
            queryset = queryset.filter(
                last_name__iexact=last_name.strip().upper())
        if first_name:
            queryset = queryset.filter(
                first_name__iexact=first_name.strip().upper())
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)

        return queryset


class BoardersPaymentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoarderPaymentsSerializer
    pagination_class = BoarderListPagination

    allowed_query_params = {"search_name", "sort_key", "sort_dir", "page"}

    def get_queryset(self):
        for param in self.request.query_params:
            if param not in self.allowed_query_params:
                raise ValidationError(
                    {"error": f"Invalid query parameter '{param}'."})

        queryset = Boarder.objects.filter(is_active=True)

        latest_payment = (
            Payment.objects
            .filter(boarder=OuterRef("pk"))
            .annotate(
                status_priority=Case(
                    When(status="PENDING", then=Value(1)),
                    When(status="CONFIRMED", then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            )
            .order_by("status_priority", "-created_at")
        )

        queryset = queryset.annotate(
            last_payment_date=Subquery(
                latest_payment.values("created_at")[:1]
            ),
            last_payment_status=Subquery(
                latest_payment.values("status")[:1]
            ),
            last_payment_priority=Subquery(
                latest_payment.values("status_priority")[:1]),
        )

        # Search by first or last name
        search_name = self.request.query_params.get("search_name")
        if search_name:
            search_name = search_name.strip()
            queryset = queryset.filter(
                Q(first_name__icontains=search_name) |
                Q(last_name__icontains=search_name)
            )

        # Sorting
        sort_map = {
            "last_name": ["last_name", "first_name"],
            "first_name": ["first_name", "last_name"],
            "last_payment_date": ["last_payment_date", "last_name", "first_name"],
            "status": ["last_payment_priority", "last_name", "first_name"],
        }

        # Safe sort_key: fallback if missing, empty, or invalid
        requested_sort_key = self.request.query_params.get(
            "sort_key") or "status"
        sort_key = requested_sort_key if requested_sort_key in sort_map else "status"

        # Default directions per column
        default_directions = {
            "last_name": "asc",
            "first_name": "asc",
            "last_payment_date": "desc",
            "status": "asc"
        }

        # Safe sort_dir: fallback if missing, empty, or invalid
        requested_sort_dir = self.request.query_params.get("sort_dir")
        sort_dir = requested_sort_dir if requested_sort_dir in [
            "asc", "desc"] else default_directions.get(sort_key, "asc")

        # Build sort order
        fields = sort_map[sort_key]
        primary_field = fields[0]

        # Build sort order (nulls always last)
        nulls_last_case = Case(
            When(**{f"{primary_field}__isnull": True}, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )

        if sort_dir == "asc":
            queryset = queryset.order_by(
                nulls_last_case, F(primary_field).asc(), *fields[1:])
        else:
            queryset = queryset.order_by(
                nulls_last_case, F(primary_field).desc(), *fields[1:])

        return queryset
