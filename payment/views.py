from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from payment.models import PaymentType, PaymentMethod
from payment.serializers import PaymentSerializer, PaymentTypeSerializer, PaymentMethodSerializer

# Create your views here.
# views.py


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data saved successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivePaymentTypeListView(ReadOnlyModelViewSet):
    queryset = PaymentType.objects.filter(is_active=True)
    serializer_class = PaymentTypeSerializer


class ActivePaymentMethodListView(ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
