from django.urls import path
from rest_framework.routers import SimpleRouter
from payment.views import PaymentView, PaymentListCreateView, ActivePaymentTypeListView, ActivePaymentMethodListView, BoarderPaymentsListView, UpdatePaymentStatusView, PaymentDetailView, PaymentView_v2

router = SimpleRouter()
router.register(r'types', ActivePaymentTypeListView,
                basename='active-payment-types')
router.register(r'methods', ActivePaymentMethodListView,
                basename='active-payment-methods')

urlpatterns = [
    path('pay/', PaymentView_v2.as_view(), name='pay'),
    path("payments/", PaymentListCreateView.as_view(), name="payment-list-create"),
    path("boarder-payments/", BoarderPaymentsListView.as_view(),
         name="boarder-payments"),
    path('update/', UpdatePaymentStatusView.as_view(),
         name='update-payment-status'),
    path("view/<int:pk>", PaymentDetailView.as_view(),
         name="view-boarder-payments")
]
urlpatterns += router.urls
