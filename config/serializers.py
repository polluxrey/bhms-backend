from rest_framework import serializers
from config.models import BrandingConfig, ContactConfig, FeatureToggle


class BrandingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandingConfig
        fields = [
            'app_name'
        ]
