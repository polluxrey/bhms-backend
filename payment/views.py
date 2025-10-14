from django.shortcuts import render
from rest_framework import viewsets
from payment.models import PaymentType, PaymentMethod
from payment.serializers import PaymentTypeSerializer, PaymentMethodSerializer

# Create your views here.
# views.py


class ActivePaymentTypeListView(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentType.objects.filter(is_active=True)
    serializer_class = PaymentTypeSerializer


class ActivePaymentMethodListView(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
