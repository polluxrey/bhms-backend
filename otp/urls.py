from django.urls import path
from otp.views import SendOTPAPIView, VerifyOTPAPIView, SendOTPAPIView_v2

urlpatterns = [
    path('send/', SendOTPAPIView_v2.as_view(), name='send-otp'),
    path('verify/', VerifyOTPAPIView.as_view(), name='verify-otp'),
]
