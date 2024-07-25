from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import SignUpViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("sign-up", SignUpViewSet, basename="sign_up")
urlpatterns = [
    *router.urls,
]
