from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    boarder_id = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    boarder_id = serializers.CharField()
    otp = serializers.CharField(max_length=6)
