from rest_framework import viewsets
from boarder.models import Boarder
from boarder.serializers import BoarderNameSerializer

# Create your views here.
# views.py


class ActiveBoarderNameListView(viewsets.ReadOnlyModelViewSet):
    queryset = Boarder.objects.filter(is_active=True).order_by(
        "last_name", "first_name", "middle_name")
    serializer_class = BoarderNameSerializer
