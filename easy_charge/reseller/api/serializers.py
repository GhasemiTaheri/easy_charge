from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from easy_charge.reseller.models import CreditRequest
from easy_charge.reseller.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "is_verify", "balance"]
        extra_kwargs = {
            "is_verify": {"read_only": True},
            "balance": {"read_only": True},
        }

    def validate(self, attrs):
        current_user = self.context.get("request").user
        if (
            self.context.get("view").action == "create"
            and current_user.vendorprofile.has_store()
        ):
            raise ValidationError(_("You create a store before!"))

        return attrs


class PublicVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name"]


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ["id", "amount", "approved"]
        extra_kwargs = {
            "approved": {"read_only": True},
        }


class ChargePhoneSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1, required=True)
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^09[0-9]{9}$",
                message=_("Phone number is not correct!"),
                code="invalid_phone_number",
            ),
        ],
        required=False,
    )
