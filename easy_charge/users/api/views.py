from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from easy_charge.users.models import CustomerProfile
from easy_charge.users.models import VendorProfile

from .serializers import CustomerSerializer
from .serializers import SignUpSerializer


class SignUpViewSet(GenericViewSet):
    serializer_class = SignUpSerializer
    permission_classes = [~IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        url_path="vendor-signup",
    )
    def vendor_signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_obj = serializer.save()
            VendorProfile.objects.create(user=user_obj)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="customer-signup",
        serializer_class=CustomerSerializer,
    )
    def customer_signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_obj = serializer.save()
            CustomerProfile.objects.create(
                user=user_obj,
                phone_number=serializer.validated_data.get("phone_number"),
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
