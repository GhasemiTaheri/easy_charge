from easy_charge.users.api.routers import urlpatterns as user_urlpatterns

app_name = "api"
urlpatterns = [
    *user_urlpatterns,
]
