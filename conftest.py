from pytest_factoryboy import register

from api.tests.factories import ApiTokenFactory
from users.tests.factories import UserFactory

register(ApiTokenFactory)
register(UserFactory)
