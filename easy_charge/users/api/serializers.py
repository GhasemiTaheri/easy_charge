from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from easy_charge.users.models import User
from easy_charge.users.models import VendorProfile


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["id", "username", "name", "password"]
        extra_kwargs = {
            "password": {
                "required": True,
                "write_only": True,
            },
        }

    def validate_password(self, data):
        return make_password(data)
