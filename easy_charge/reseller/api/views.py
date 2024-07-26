from django.db import transaction
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from easy_charge.reseller.models import CreditRequest
from easy_charge.reseller.models import Vendor
from easy_charge.users.models import User  # noqa: TCH001
from easy_charge.utility.api import IsVendorUser

from .permissions import CreditRequestPermission
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
    queryset = CreditRequest.objects.all()
    permission_classes = [CreditRequestPermission]

    def perform_create(self, serializer) -> None:
        return serializer.save(vendor=self.request.user.vendorprofile.vendor)

    def get_queryset(self) -> QuerySet:
        current_user: User = self.request.user

        if current_user.get_role() == "vendor":
            return CreditRequest.scoop_objects.filter_by_user(current_user)

        return super().get_queryset()

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def approve_request(self, request):
        obj: CreditRequest = self.get_object()

        if obj.approved:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                obj.approved = True
                obj.save()

                vendor_obj = Vendor.objects.select_for_update().get(id=obj.vendor_id)
                vendor_obj.balance += obj.amount
                vendor_obj.save()
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
