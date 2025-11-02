from rest_framework import serializers
from payment.models import Payment, PaymentType, PaymentMethod


from rest_framework import serializers
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    extra_fields = ["created_at_date_display", "created_at_datetime_display",
                    "payment_method_name", "payment_type_name", "boarder_full_name"]

    created_at_date_display = serializers.SerializerMethodField()
    created_at_datetime_display = serializers.SerializerMethodField()
    payment_method_name = serializers.CharField(
        source="payment_method.name", read_only=True)
    payment_type_name = serializers.CharField(
        source="payment_type.name", read_only=True)
    boarder_full_name = serializers.CharField(
        source="boarder.full_name", read_only=True)

    class Meta:
        model = Payment
        # Include all fields by default
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            # Always include method fields if requested
            for extra_field in self.extra_fields:
                if extra_field in fields:
                    allowed.add(extra_field)
            for field_name in list(self.fields):
                if field_name not in allowed:
                    self.fields.pop(field_name)

    def get_created_at_date_display(self, obj):
        return obj.created_at.strftime("%B %d, %Y")

    def get_created_at_datetime_display(self, obj):
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")


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
