from rest_framework import serializers
from payment.models import Payment, PaymentType, PaymentMethod


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["boarder", "payment_type", "payment_method",
                  "amount", "description", "receipt"]


class PaymentListSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ["boarder", "date", "amount", "status"]

    def get_date(self, obj):
        return obj.created_at.date().strftime("%Y-%m-%d")


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ["id", "name", "code"]


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name", "code"]
