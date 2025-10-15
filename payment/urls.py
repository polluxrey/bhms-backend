from django.urls import path
from rest_framework.routers import SimpleRouter
from payment.views import PaymentView, ActivePaymentTypeListView, ActivePaymentMethodListView

router = SimpleRouter()
router.register(r'types', ActivePaymentTypeListView,
                basename='active-payment-types')
router.register(r'methods', ActivePaymentMethodListView,
                basename='active-payment-methods')

urlpatterns = [
    path('pay/', PaymentView.as_view(), name='pay'),
]
urlpatterns += router.urls
