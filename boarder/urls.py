from rest_framework.routers import SimpleRouter
from boarder.views import ActiveBoarderNameListView

router = SimpleRouter()
router.register(r'names', ActiveBoarderNameListView,
                basename='active-boarder-names')
urlpatterns = router.urls
