from django import apps
from django.utils import translation


class UsersConfig(apps.AppConfig):
    name = "bitbank.transfers"
    verbose_name = translation.gettext_lazy("Transfers")

    def ready(self):
        try:
            import bitbank.transfers.signals  # noqa F401
        except ImportError:
            pass
