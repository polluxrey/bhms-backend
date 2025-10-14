from rest_framework import serializers
from boarder.models import Boarder


class BoarderNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Boarder
        fields = ["id", "name"]

    def get_name(self, obj):
        return f"{obj.last_name}, {obj.first_name} {obj.middle_name}".strip()
