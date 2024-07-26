from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class CreditRequestPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        current_user = request.user
        user_role = current_user.get_role()

        if user_role == "vendor" and current_user.vendorprofile.has_store():
            return True

        return bool(user_role == "admin" and request.method in SAFE_METHODS)
