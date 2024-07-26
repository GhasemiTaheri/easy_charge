from easy_charge.reseller.api.routers import urlpatterns as reseller_urlpatterns
from easy_charge.users.api.routers import urlpatterns as user_urlpatterns

app_name = "api"
urlpatterns = [
    *user_urlpatterns,
    *reseller_urlpatterns,
]
