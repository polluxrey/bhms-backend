from django.urls import path
from otp.views import SendOTPAPIView, VerifyOTPAPIView

urlpatterns = [
    path('send/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify/', VerifyOTPAPIView.as_view(), name='verify-otp'),
]
