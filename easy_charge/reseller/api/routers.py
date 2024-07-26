from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import CreditRequestViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("credit-request", CreditRequestViewSet, basename="credit_request")
urlpatterns = [
    *router.urls,
]
