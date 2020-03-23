from factory import DjangoModelFactory, SubFactory

from main.tests.factories import LocationFactory
from users.tests.factories import UserFactory

from ..models import ApiToken


class ApiTokenFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = ApiToken

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super()._after_postgeneration(obj, create, results)
        obj.header = f"Bearer {obj.token}"
