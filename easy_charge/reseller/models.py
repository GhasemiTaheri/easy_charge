import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from easy_charge.utility.db import TimeBaseModel


class Vendor(TimeBaseModel):
    id = models.UUIDField(
        _("Id"),
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(_("Vendor Name"), max_length=50)
    owner = models.OneToOneField(
        "users.VendorProfile",
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_verify": True,
        },
        verbose_name=_("Owner"),
    )
    is_verify = models.BooleanField(_("Is Verified"), default=False)
    balance = models.PositiveIntegerField(_("Balance"), default=0)

    def __str__(self) -> str:
        return self.name


class CreditRequest(TimeBaseModel):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        limit_choices_to={"is_verify": True},
        verbose_name=_("Vendor"),
    )
    amount = models.PositiveIntegerField(_("Amount"))
    approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.vendor} {self.ammount}"


class SellHistory(TimeBaseModel):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        verbose_name=_("Vendor"),
    )
    customer = models.ForeignKey(
        "users.CustomerProfile",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Charge Buyer"),
    )
    amount = models.PositiveIntegerField(
        _("Charge Amount"),
    )
