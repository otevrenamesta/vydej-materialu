import pytest
from django.core.management import call_command
from pytest_factoryboy import register

from api.tests.factories import ApiTokenFactory
from main.tests.factories import LocationFactory, RegionFactory
from users.tests.factories import UserFactory

register(ApiTokenFactory)
register(LocationFactory)
register(RegionFactory)
register(UserFactory)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("load_groups")
