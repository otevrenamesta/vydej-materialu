from factory import DjangoModelFactory, SubFactory

from users.tests.factories import UserFactory

from ..models import ApiToken


class ApiTokenFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = ApiToken
