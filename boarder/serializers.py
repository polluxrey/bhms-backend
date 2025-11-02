from django.conf import settings
from rest_framework import serializers
from boarder.models import Boarder
from bhms.utils import parse_room_code, format_date
from bhms.choices import PaymentStatus


class BoarderNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Boarder
        fields = ["id", "name"]

    def get_name(self, obj):
        return obj.full_name


class BoarderListSerializer(serializers.ModelSerializer):
    room_number = serializers.SerializerMethodField()

    class Meta:
        model = Boarder
        fields = ['id', 'full_name', 'room_number', 'is_active']

    def get_room_number(self, obj):
        return parse_room_code(obj.room_number)


class BoarderDisplaySerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    year_level = serializers.CharField(
        source="get_year_level_display", read_only=True)
    sex = serializers.CharField(source="get_sex_display", read_only=True)
    degree_program = serializers.CharField(
        source="get_degree_program_display", read_only=True)
    profile_photo_url = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    move_in_date = serializers.SerializerMethodField()
    move_out_date = serializers.SerializerMethodField()

    class Meta:
        model = Boarder
        fields = ["full_name", "date_of_birth", "sex",
                  "full_address", "degree_program", "year_level", "email", "phone_number", "room_number", "move_in_date", "move_out_date", "is_active", "profile_photo_url"]

    def get_date_of_birth(self, obj):
        return format_date(obj.date_of_birth)

    def get_move_in_date(self, obj):
        return format_date(obj.move_in_date)

    def get_move_out_date(self, obj):
        return format_date(obj.move_out_date)

    def get_profile_photo_url(self, obj):
        request = self.context.get('request')

        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return request.build_absolute_uri(obj.profile_photo.url) if request else obj.profile_photo.url

        default_photo_url = f"{settings.MEDIA_URL}assets/default-profile-photo.png"
        return request.build_absolute_uri(default_photo_url) if request else default_photo_url

    def get_room_number(self, obj):
        return parse_room_code(obj.room_number)


class BoarderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boarder
        fields = '__all__'


class BoarderPaymentsSerializer(serializers.ModelSerializer):
    last_payment_date = serializers.SerializerMethodField()
    last_payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Boarder
        fields = ["id", "first_name", "last_name", "full_name",
                  "last_payment_date", "last_payment_status"]

    def get_last_payment_date(self, obj):
        if not obj.last_payment_date:
            return None  # handle boarders with no payments

        # Format: October 31, 2025 9:11 AM
        return obj.last_payment_date.strftime("%B %d, %Y %I:%M %p")

    def get_last_payment_status(self, obj):
        if not obj.last_payment_date:
            return None

        return (
            PaymentStatus(obj.last_payment_status).label
            if obj.last_payment_status
            else "Unknown"
        )
