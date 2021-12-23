import pytest

from bitbank.users.models import User
from bitbank.users.tests import factories
from bitbank.users import errors

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_transfer_satoshi():
    to_user = factories.UserFactory(username="to_user", satoshis=100)
    from_user = factories.UserFactory(username="from_user", satoshis=100)

    User.transfer_satoshi(
        from_username=from_user.username, to_username=to_user.username, amount=100
    )

    to_user = User.objects.get(username="to_user")
    from_user = User.objects.get(username="from_user")
    assert to_user.satoshis == 200
    assert from_user.satoshis == 0


def test_user_transfer_satoshi_zero():
    to_user = factories.UserFactory(username="to_user", satoshis=100)
    from_user = factories.UserFactory(username="from_user", satoshis=100)

    User.transfer_satoshi(
        from_username=from_user.username, to_username=to_user.username, amount=0
    )

    to_user = User.objects.get(username="to_user")
    from_user = User.objects.get(username="from_user")
    assert to_user.satoshis == 100
    assert from_user.satoshis == 100


def test_user_transfer_satoshi_not_enough_satoshis():
    to_user = factories.UserFactory(username="to_user", satoshis=100)
    from_user = factories.UserFactory(username="from_user", satoshis=99)

    with pytest.raises(errors.UnableToTransferSatoshis):
        User.transfer_satoshi(
            from_username=from_user.username, to_username=to_user.username, amount=100
        )

    to_user = User.objects.get(username="to_user")
    from_user = User.objects.get(username="from_user")
    assert from_user.satoshis == 99
    assert to_user.satoshis == 100
