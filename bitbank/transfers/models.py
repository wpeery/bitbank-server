from django.db import models as db_models
from bitbank.users import models as user_models
from django.utils import translation


class SatoshiTransfer(db_models.Model):
    """Model for a transfer of satoshi."""

    amount = db_models.PositiveBigIntegerField(
        translation.gettext_lazy("Amount of satoshis transfered")
    )
    to_user = db_models.ForeignKey(
        user_models.User,
        related_name="incoming_satoshi",
        on_delete=db_models.DO_NOTHING,
    )
    from_user = db_models.ForeignKey(
        user_models.User,
        related_name="outgoing_satoshi",
        on_delete=db_models.DO_NOTHING,
    )
    timestamp = db_models.DateTimeField(auto_now_add=True)
