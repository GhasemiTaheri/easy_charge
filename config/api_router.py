from django.urls import include
from django.urls import path

from easy_charge.reseller.api.routers import urlpatterns as reseller_urlpatterns
from easy_charge.users.api.routers import urlpatterns as user_urlpatterns

app_name = "api"
urlpatterns = [
    path("users/", include(user_urlpatterns)),
    path("reseller/", include(reseller_urlpatterns)),
]
