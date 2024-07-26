from django.contrib import admin
from django.db import transaction

from .models import CreditRequest
from .models import SellHistory
from .models import Vendor


def verify_vendors(modeladmin, request, queryset):
    for vendor in queryset.filter(is_verify=False):
        vendor.is_verify = True
        vendor.save()


verify_vendors.short_description = "Verify selected vendors"


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "is_verify", "balance"]
    list_filter = ("is_verify", "created_at")
    search_fields = ["name"]
    ordering = ("-created_at",)
    actions = (verify_vendors,)


def approve_credit_request(modeladmin, request, queryset):
    for credit_request in queryset.filter(approved=False):
        with transaction.atomic():
            vendor_obj = Vendor.objects.select_for_update().get(
                id=credit_request.vendor_id  # noqa: COM812
            )
            vendor_obj.balance += credit_request.amount
            vendor_obj.save()
            credit_request.approved = True
            credit_request.save()


approve_credit_request.short_description = "Approve selected credit request"


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ["vendor", "amount", "approved", "created_at"]
    list_filter = ("approved", "created_at")
    ordering = ("-created_at",)
    actions = (approve_credit_request,)


@admin.register(SellHistory)
class SellHistoryAdmin(admin.ModelAdmin):
    list_display = ["vendor", "customer", "phone_number", "amount", "created_at"]
    list_filter = ("created_at",)
    ordering = ("-amount",)
