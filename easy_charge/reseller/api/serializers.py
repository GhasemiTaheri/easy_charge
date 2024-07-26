from rest_framework import serializers

from easy_charge.reseller.models import CreditRequest


class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ["vendor", "amount"]
        extra_kwargs = {"vendor": {"required": False}}
