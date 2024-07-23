import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "easy_charge.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import easy_charge.users.signals  # noqa: F401
