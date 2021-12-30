import pytest

from rest_framework import test
from bitbank.users.models import User
from bitbank.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def api_client() -> test.APIClient:
    return test.APIClient()
