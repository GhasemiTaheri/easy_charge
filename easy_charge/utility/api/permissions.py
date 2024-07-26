from rest_framework.permissions import BasePermission


class IsVendorUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.get_role() == "vendor" and request.user.is_authenticated  # noqa: COM812
        )


class StorOwnerVendor(BasePermission):
    def has_permission(self, request, view) -> bool:
        current_user = request.user
        user_role = current_user.get_role()

        return bool(user_role == "vendor" and current_user.vendorprofile.has_store())


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.get_role() == "customer" and request.user.is_authenticated  # noqa: COM812
        )
