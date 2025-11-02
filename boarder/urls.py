from rest_framework.routers import SimpleRouter
from boarder.views import ActiveBoarderNameListView, BoarderViewSet, BoardersPaymentsViewSet

router = SimpleRouter()
router.register(r'names', ActiveBoarderNameListView,
                basename='active-boarder-names')
router.register(r'boarders-payments', BoardersPaymentsViewSet,
                basename='boarders-payments')
router.register(r'', BoarderViewSet, basename='boarder')


urlpatterns = router.urls
