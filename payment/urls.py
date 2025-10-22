from django.urls import path
from rest_framework.routers import SimpleRouter
from payment.views import PaymentView, PaymentListCreateView, ActivePaymentTypeListView, ActivePaymentMethodListView

router = SimpleRouter()
router.register(r'types', ActivePaymentTypeListView,
                basename='active-payment-types')
router.register(r'methods', ActivePaymentMethodListView,
                basename='active-payment-methods')

urlpatterns = [
    path('pay/', PaymentView.as_view(), name='pay'),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list-create"),
]
urlpatterns += router.urls
