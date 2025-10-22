from django.urls import path
from service_request.views import ServiceRequestView, ServiceRequestLookupView, ServiceRequestTypeChoicesView

urlpatterns = [
    path('submit/', ServiceRequestView.as_view(), name='submit-request'),
    path("view/", ServiceRequestLookupView.as_view(), name="view-request"),
    path("types/", ServiceRequestTypeChoicesView.as_view(), name="request-types")
]
