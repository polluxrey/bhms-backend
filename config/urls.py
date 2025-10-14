from django.urls import path
from config.views import BrandingConfigView

urlpatterns = [
    path('branding/', BrandingConfigView.as_view(), name='branding-config'),
]
