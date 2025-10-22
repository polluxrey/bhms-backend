from rest_framework import status, generics, exceptions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from payment.models import Payment, PaymentType, PaymentMethod
from payment.serializers import PaymentSerializer, PaymentListSerializer, PaymentTypeSerializer, PaymentMethodSerializer
from payment.pagination import PaymentPagination

# Create your views here.
# views.py


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListCreateView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = PaymentPagination

    def get_queryset(self):
        boarder_id = self.request.query_params.get("boarderId")
        if not boarder_id:
            raise exceptions.ValidationError(
                {"detail": "boarderId query parameter is required."})
        return Payment.objects.filter(boarder=boarder_id).order_by("-created_at")


class ActivePaymentTypeListView(ReadOnlyModelViewSet):
    queryset = PaymentType.objects.filter(is_active=True)
    serializer_class = PaymentTypeSerializer


class ActivePaymentMethodListView(ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
