from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from .views import MeApiView
from .views import SignUpViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("sign-up", SignUpViewSet, basename="sign_up")
urlpatterns = [
    *router.urls,
    path("me/", MeApiView.as_view(), name="me"),
]
