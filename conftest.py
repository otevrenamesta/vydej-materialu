from pytest_factoryboy import register

from api.tests.factories import ApiTokenFactory
from main.tests.factories import LocationFactory, RegionFactory
from users.tests.factories import UserFactory

register(ApiTokenFactory)
register(LocationFactory)
register(RegionFactory)
register(UserFactory)
