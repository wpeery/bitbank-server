from django.contrib.auth import models as auth_models
from django.db import models as db_models
from django import urls
from django.utils import translation


class User(auth_models.AbstractUser):
    """Default user for bitbank-server."""

    #: First and last name do not cover name patterns around the globe
    name = db_models.CharField(
        translation.gettext_lazy("Name of User"), blank=True, max_length=255
    )
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    satoshis = db_models.PositiveBigIntegerField(
        translation.gettext_lazy("Amount of satoshis owned"), default=0
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return urls.reverse("users:detail", kwargs={"username": self.username})
