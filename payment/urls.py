from rest_framework.routers import SimpleRouter
from payment.views import ActivePaymentTypeListView, ActivePaymentMethodListView

router = SimpleRouter()
router.register(r'types', ActivePaymentTypeListView,
                basename='active-payment-types')
router.register(r'methods', ActivePaymentMethodListView,
                basename='active-payment-methods')
urlpatterns = router.urls
