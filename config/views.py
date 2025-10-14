from rest_framework.views import APIView
from rest_framework.response import Response
from config.models import BrandingConfig
from config.serializers import BrandingConfigSerializer

# Create your views here.


class BrandingConfigView(APIView):
    def get(self, request):
        obj = BrandingConfig.objects.first()
        serializer = BrandingConfigSerializer(obj)
        return Response(serializer.data)
