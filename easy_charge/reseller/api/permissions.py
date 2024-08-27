from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class CreditRequestObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return request.method in SAFE_METHODS or not bool(obj.approved)


class CustomerSafeRequestPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.is_authenticated
            and request.user.get_role() == "customer"
            and request.method in SAFE_METHODS
        )
