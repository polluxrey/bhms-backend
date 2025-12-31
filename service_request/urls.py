from django.urls import path, include
from rest_framework.routers import SimpleRouter
from service_request.views import ServiceRequestView, ServiceRequestLookupView, ServiceRequestTypeChoicesView, ServiceRequestViewSet, RequestStatusAPIView

router = SimpleRouter()
router.register(r'', ServiceRequestViewSet, basename='requests')

urlpatterns = [
    path('submit/', ServiceRequestView.as_view(), name='submit-request'),
    path("view/", ServiceRequestLookupView.as_view(), name="view-request"),
    path("types/", ServiceRequestTypeChoicesView.as_view(), name="request-types"),
    path("statuses/", RequestStatusAPIView.as_view(), name="request-statuses"),
    path('', include(router.urls))
]
