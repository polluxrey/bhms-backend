from rest_framework import viewsets
from module.models import Module
from module.serializers import ModuleSerializer

# Create your views here.


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.order_by('order')
    serializer_class = ModuleSerializer
