import pytest

from easy_charge.users.models import User
from easy_charge.users.tests.factories import UserFactory


@pytest.fixture()
def user(db) -> User:
    return UserFactory()
