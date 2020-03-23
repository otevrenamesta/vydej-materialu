from factory import DjangoModelFactory, Faker, SubFactory

from users.tests.factories import UserFactory

from ..models import Location, LocationStaff, Region


class RegionFactory(DjangoModelFactory):
    name = Faker("city")
    about = Faker("paragraph")

    class Meta:
        model = Region
        django_get_or_create = ["name"]


class LocationFactory(DjangoModelFactory):
    name = Faker("company")
    region = SubFactory(RegionFactory)
    about = Faker("paragraph")
    address = Faker("address")
    phone = Faker("random_number", digits=9)

    class Meta:
        model = Location
        django_get_or_create = ["name", "region"]


class LocationStaffFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    location = SubFactory(LocationFactory)

    class Meta:
        model = LocationStaff
