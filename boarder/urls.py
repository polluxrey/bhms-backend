from django.urls import path
from rest_framework.routers import SimpleRouter
from boarder.views import ActiveBoarderNameListView, BoarderViewSet, BoardersPaymentsViewSet, RoomNumberAPIView, DegreeProgramAPIView, YearLevelAPIView, SchoolAPIView

router = SimpleRouter()
router.register(r'names', ActiveBoarderNameListView,
                basename='active-boarder-names')
router.register(r'boarders-payments', BoardersPaymentsViewSet,
                basename='boarders-payments')
router.register(r'', BoarderViewSet, basename='boarder')


urlpatterns = [
    path('rooms/', RoomNumberAPIView.as_view(),
         name='room-numbers'),
    path('academic-programs/', DegreeProgramAPIView.as_view(),
         name='academic-programs'),
    path('year-levels/', YearLevelAPIView.as_view(),
         name='year-levels'),
    path('schools/', SchoolAPIView.as_view(),
         name='year-levels'),
]

urlpatterns += router.urls
