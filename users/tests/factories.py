from django.conf import settings
from factory import DjangoModelFactory, Faker


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ["username"]
