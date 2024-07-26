from django.db import transaction
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from easy_charge.reseller.models import CreditRequest
from easy_charge.reseller.models import SellHistory
from easy_charge.reseller.models import Vendor
from easy_charge.users.models import CustomerProfile  # noqa: TCH001
from easy_charge.users.models import User  # noqa: TCH001
from easy_charge.utility.api import IsCustomerUser
from easy_charge.utility.api import IsVendorUser
from easy_charge.utility.api import StorOwnerVendor

from .permissions import CreditRequestObjectPermission
from .permissions import CustomerSafeRequestPermission
from .serializers import ChargePhoneSerializer
from .serializers import CreditRequestSerializer
from .serializers import PublicVendorSerializer
from .serializers import VendorSerializer


class VendorViewSet(ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [
        IsVendorUser | CustomerSafeRequestPermission  # noqa: COM812
    ]

    def get_queryset(self) -> QuerySet:
        if self.request.user.get_role() == "customer":
            return Vendor.objects.filter(is_verify=True)
        return Vendor.objects.filter(owner=self.request.user.vendorprofile.id)

    def get_serializer_class(self):
        if self.request.user.get_role() == "customer":
            return PublicVendorSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user.vendorprofile)


class CreditRequestViewSet(ModelViewSet):
    serializer_class = CreditRequestSerializer
    permission_classes = [StorOwnerVendor & CreditRequestObjectPermission]

    def perform_create(self, serializer) -> None:
        return serializer.save(vendor=self.request.user.vendorprofile.vendor)

    def get_queryset(self) -> QuerySet:
        current_user: User = self.request.user
        return CreditRequest.scoop_objects.filter_by_user(current_user)


class ChargePhoneNumberView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request, vendor_id):
        serializer = ChargePhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor: Vendor = get_object_or_404(
            Vendor.objects.filter(is_verify=True).select_for_update(),
            id=str(vendor_id),
        )
        current_customer: CustomerProfile = request.user.customerprofile

        with transaction.atomic():
            if int(vendor.balance) < int(serializer.validated_data.get("amount")):
                raise ValidationError(_("Please try later or use another vendor!"))

            vendor.balance -= serializer.validated_data.get("amount")
            vendor.save()

            sellhistory_data = {
                "vendor": vendor,
                "amount": serializer.validated_data.get("amount"),
            }
            if serializer.validated_data.get("phone_number"):
                sellhistory_data["phone_number"] = serializer.validated_data.get(
                    "phone_number"  # noqa: COM812
                )
            else:
                current_customer.balance += serializer.validated_data.get("amount")
                current_customer.save()
                sellhistory_data["customer"] = current_customer

            SellHistory.objects.create(**sellhistory_data)

        return Response(
            {"status": _("successful operation!")},
            status=status.HTTP_200_OK,
        )
