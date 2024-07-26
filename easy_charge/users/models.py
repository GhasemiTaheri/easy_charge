from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from easy_charge.utility.db import TimeBaseModel


class User(AbstractUser):
    """
    Default custom user model.
    """

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_role(self):
        if hasattr(self, "vendorprofile") and self.vendorprofile:
            return "vendor"
        elif hasattr(self, "customerprofile") and self.customerprofile:
            return "customer"
        else:
            return "admin"


class VendorProfile(TimeBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    is_verify = models.BooleanField(_("Is Verified"), default=True)

    def has_stor(self):
        return hasattr(self, "vendor")


class CustomerProfile(TimeBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    phone_number = models.CharField(
        _("Phone Number"),
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^09[0-9]{9}$",
                message=_("Phone number is not correct!"),
                code="invalid_phone_number",
            ),
        ],
    )
    balance = models.PositiveIntegerField(_("Balance"), default=0)


class VendorUser(User):
    class Meta:
        proxy = True

    class VendorManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            return super().get_queryset().filter(vendorprofile__isnull=False)

    objects = VendorManager()

    @property
    def extra(self):
        return self.vendorprofile


class CustomerUser(User):
    class Meta:
        proxy = True

    class CustomerManager(models.Manager):
        def get_queryset(self) -> models.QuerySet:
            queryset = super().get_queryset()
            return queryset.filter(customerprofile__isnull=False)

    objects = CustomerManager()

    @property
    def extra(self) -> CustomerProfile:
        return self.customerprofile
