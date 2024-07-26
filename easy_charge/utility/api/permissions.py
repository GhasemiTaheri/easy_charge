from rest_framework.permissions import BasePermission


class IsVendorUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.get_role() == "vendor" and request.user.is_authenticated  # noqa: COM812
        )

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.get_role() == "customer" and request.user.is_authenticated  # noqa: COM812
        )
