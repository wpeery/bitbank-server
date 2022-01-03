import pytest

from django import urls
from rest_framework import test

from bitbank import api_errors
from bitbank.users import models as user_models
from bitbank.transfers import models as transfer_models
from bitbank.users.tests import factories as user_factories


pytestmark = pytest.mark.django_db

TRANSFER_URL = urls.reverse("api:transfers-transfer-satoshi")


class TestTransferViewSet:
    def test_transfer_satoshi(self, user: user_models.User, api_client: test.APIClient):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        api_client.force_authenticate(user=from_user)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": user.username, "amount": 100},
        )
        assert response.data == {"success": True}
        assert user_models.User.objects.get(username=from_user.username).satoshis == 900
        assert user_models.User.objects.get(username=user.username).satoshis == 100

        transfer = transfer_models.SatoshiTransfer.objects.get(from_user=from_user)
        assert transfer.amount == 100
        assert transfer.to_user == user

    def test_transfer_satoshi_not_logged_in(
        self, user: user_models.User, api_client: test.APIClient
    ):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": user.username, "amount": 100},
        )
        assert response.status_code == 403
        assert (
            user_models.User.objects.get(username=from_user.username).satoshis == 1000
        )
        assert user_models.User.objects.get(username=user.username).satoshis == 0

    def test_transfer_satoshi_not_enough_satoshis(
        self, user: user_models.User, api_client: test.APIClient
    ):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        api_client.force_authenticate(user=from_user)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": user.username, "amount": 10000},
        )
        assert response.data["error_code"] == api_errors.NOT_ENOUGH_FUNDS
        assert (
            user_models.User.objects.get(username=from_user.username).satoshis == 1000
        )
        assert user_models.User.objects.get(username=user.username).satoshis == 0

    @pytest.mark.parametrize(
        "to_username,amount",
        [
            ("", 100),
            ("some_user", -1),
            ("some_user", "5d"),
        ],
    )
    def test_transfer_satoshi_invalid_params(
        self, to_username, amount, api_client: test.APIClient
    ):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        api_client.force_authenticate(user=from_user)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": to_username, "amount": amount},
        )
        assert response.status_code == 400
        assert (
            user_models.User.objects.get(username=from_user.username).satoshis == 1000
        )

    def test_transfer_satoshi_to_self(self, api_client: test.APIClient):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        api_client.force_authenticate(user=from_user)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": from_user.username, "amount": 100},
        )
        assert response.data["error_code"] == api_errors.UNABLE_TO_TRANSFER_FUNDS
        assert response.data["details"] == "Cannot transfer funds to self"
        assert (
            user_models.User.objects.get(username=from_user.username).satoshis == 1000
        )

    def test_transfer_satoshi_user_does_not_exist(self, api_client: test.APIClient):
        from_user = user_factories.UserFactory(username="from_user", satoshis=1000)
        api_client.force_authenticate(user=from_user)
        response = api_client.post(
            TRANSFER_URL,
            {"to_username": "does-not-exist", "amount": 1000},
        )
        assert response.data["error_code"] == api_errors.ENTITY_DOES_NOT_EXIST
        assert (
            user_models.User.objects.get(username=from_user.username).satoshis == 1000
        )
