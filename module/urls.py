from rest_framework.routers import SimpleRouter
from .views import ModuleViewSet

router = SimpleRouter()
router.register(r'modules', ModuleViewSet, basename='module')

urlpatterns = router.urls
