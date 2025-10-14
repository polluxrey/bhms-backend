from rest_framework import serializers
from module.models import Module


class ModuleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'image_url',
            'redirect_url',
            'order',
            'is_active',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
