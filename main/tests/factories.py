from factory import DjangoModelFactory, Faker, SubFactory

from ..models import Location, Region


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
