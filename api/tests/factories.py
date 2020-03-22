from factory import DjangoModelFactory, SubFactory

from main.tests.factories import LocationFactory
from users.tests.factories import UserFactory

from ..models import ApiToken


class ApiTokenFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = ApiToken
