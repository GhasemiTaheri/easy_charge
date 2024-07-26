from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet

from easy_charge.reseller.models import CreditRequest
from easy_charge.reseller.models import Vendor
from easy_charge.users.models import User  # noqa: TCH001
from easy_charge.utility.api import IsVendorUser
from easy_charge.utility.api import StorOwnerVendor

from .permissions import CreditRequestObjectPermission
from .serializers import CreditRequestSerializer
from .serializers import VendorSerializer


class VendorViewSet(ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [IsVendorUser]

    def get_queryset(self) -> QuerySet:
        return Vendor.objects.filter(owner=self.request.user.vendorprofile.id)

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
