from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import CreditRequestViewSet
from .views import VendorViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("vendor", VendorViewSet, basename="vendor")
router.register("credit-request", CreditRequestViewSet, basename="credit_request")

urlpatterns = [
    *router.urls,
]
