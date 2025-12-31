from rest_framework import serializers
from service_request.models import ServiceRequest
from bhms.choices import RequestType


class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ["boarder", "request_type", "description", "attachment"]


class ServiceRequestDetailSerializer(serializers.ModelSerializer):
    boarder_full_name = serializers.SerializerMethodField()
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            "reference_number",
            "boarder_full_name",
            "request_type",
            "description",
            "status",
            "admin_remarks",
            "attachment_url",
            "created_at",
            "updated_at",
        ]

    def get_boarder_full_name(self, obj):
        boarder = obj.boarder
        if boarder.middle_name:
            return f"{boarder.last_name}, {boarder.first_name} {boarder.middle_name}"
        return f"{boarder.last_name}, {boarder.first_name}"

    def get_attachment_url(self, obj):
        request = self.context.get('request')
        print(request)
        if obj.attachment and request:
            return request.build_absolute_uri(obj.attachment.url)
        return None


class ServiceRequestTypeSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=15)
    label = serializers.CharField(max_length=25)


class ServiceRequestListSerializer(serializers.ModelSerializer):
    boarder_full_name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequest
        fields = [
            "reference_number",
            "boarder_full_name",
            "request_type",
            "status",
            "created_at",
        ]

    def get_boarder_full_name(self, obj):
        boarder = obj.boarder
        if boarder.middle_name:
            return f"{boarder.last_name}, {boarder.first_name} {boarder.middle_name}"
        return f"{boarder.last_name}, {boarder.first_name}"
