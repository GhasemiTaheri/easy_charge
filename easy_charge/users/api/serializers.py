from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from easy_charge.users.models import CustomerProfile
from easy_charge.users.models import User
from easy_charge.users.models import VendorProfile


class SignUpSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="ID", read_only=True)
    username = serializers.CharField(
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."  # noqa: COM812
        ),
        max_length=150,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    name = serializers.CharField(
        label=_("Name of User"),
        max_length=255,
        allow_blank=True,
        required=False,
    )
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate_password(self, data):
        return make_password(data)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CustomerSerializer(SignUpSerializer):
    phone_number = serializers.CharField(
        label=_("Phone Number"),
        validators=[
            RegexValidator(
                regex=r"^09[0-9]{9}$",
                message=_("Phone number is not correct!"),
                code="invalid_phone_number",
            ),
            UniqueValidator(queryset=CustomerProfile.objects.all()),
        ],
        write_only=True,
    )

    def create(self, validated_data):
        user_data = {**validated_data}
        del user_data["phone_number"]
        return super().create(user_data)


class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ["is_verify"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["phone_number", "balance"]


class MeSerializer(serializers.ModelSerializer):
    extra = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "name", "extra"]

    def get_extra(self, obj):
        if obj.get_role() == "vendor":
            return VendorProfileSerializer(instance=obj.vendorprofile).data
        if obj.get_role() == "customer":
            return CustomerProfileSerializer(obj.customerprofile).data

        return None
