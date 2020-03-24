import json
from random import randint
from types import SimpleNamespace

import pytest
from django.urls import reverse
from faker import Faker

from main.models import Dispensed, LocationStaff

pytestmark = pytest.mark.django_db

fake = Faker()


@pytest.fixture
def staff(location_staff_factory, api_token):
    location_staff_factory(
        user=api_token.user, location=api_token.location, status=LocationStaff.VOLUNTEER
    )
    return SimpleNamespace(
        user=api_token.user, location=api_token.location, api_token=api_token
    )


@pytest.mark.parametrize("url", ["api:material"])
def test_get__no_token(client, snapshot, url):
    response = client.get(reverse(url))

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


@pytest.mark.parametrize("url", ["api:material"])
def test_get__not_staff(client, snapshot, api_token, url):
    response = client.get(reverse(url), HTTP_AUTHORIZATION=api_token.header)

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


@pytest.mark.parametrize("url", ["api:dispense", "api:validate"])
def test_post__no_token(client, snapshot, url):
    response = client.post(reverse(url))

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


@pytest.mark.parametrize("url", ["api:dispense", "api:validate"])
def test_post__not_staff(client, snapshot, api_token, url):
    response = client.post(reverse(url), HTTP_AUTHORIZATION=api_token.header)

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


@pytest.mark.parametrize("url", ["api:dispense", "api:validate"])
def test_post__wrong_payload(client, snapshot, staff, url):
    response = client.post(
        reverse(url), "abc", "text/plain", HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_login__missing_payload(client, snapshot):
    response = client.post(reverse("api:login"))

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_login__wrong_payload(client, snapshot):
    response = client.post(reverse("api:login"), "xyz", "text/plain")

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_login__unknown_user(client, snapshot, location):
    payload = {
        "login": fake.user_name(),
        "password": fake.password(),
        "location": str(location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_login__unknown_location(client, snapshot, user):
    password = fake.password()
    user.set_password(password)
    user.save()
    payload = {
        "login": user.email,
        "password": password,
        "location": str(fake.pyint()),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 404
    snapshot.assert_match(json.loads(response.content))


def test_login__not_staff(client, snapshot, user, location):
    password = fake.password()
    user.set_password(password)
    user.save()
    payload = {
        "login": user.email,
        "password": password,
        "location": str(location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_login__staff_pending(client, snapshot, location_staff_factory):
    ls = location_staff_factory(status=LocationStaff.PENDING)
    password = fake.password()
    ls.user.set_password(password)
    ls.user.save()
    payload = {
        "login": ls.user.email,
        "password": password,
        "location": str(ls.location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_login__staff_admin(client, location_staff_factory):
    ls = location_staff_factory(status=LocationStaff.ADMIN)
    password = fake.password()
    ls.user.set_password(password)
    ls.user.save()
    payload = {
        "login": ls.user.email,
        "password": password,
        "location": str(ls.location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content["result"] == "success"
    assert isinstance(content["token"], str)
    assert len(content["token"]) > 50


def test_login__staff_volunteer(client, location_staff_factory):
    ls = location_staff_factory(status=LocationStaff.VOLUNTEER)
    password = fake.password()
    ls.user.set_password(password)
    ls.user.save()
    payload = {
        "login": ls.user.email,
        "password": password,
        "location": str(ls.location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content["result"] == "success"
    assert isinstance(content["token"], str)
    assert len(content["token"]) > 50


def test_material__nothing_available(client, snapshot, staff):
    response = client.get(
        reverse("api:material"), HTTP_AUTHORIZATION=staff.api_token.header
    )

    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content))


def test_material(client, snapshot, material_record_factory, staff):
    material_record_factory(
        location=staff.location, material__id=1, material__name="Rouška"
    )
    material_record_factory(
        location=staff.location, material__id=2, material__name="Respirátor"
    )
    material_record_factory(material__id=3)

    response = client.get(
        reverse("api:material"), HTTP_AUTHORIZATION=staff.api_token.header
    )

    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content))


def test_dispense__wrong_material(client, snapshot, staff, material_record_factory):
    material_record_factory(location=staff.location, material__id=1)
    material_record_factory(material__id=2)
    payload = {"idcardno": 123456789, "material": [{"id": 2, "quantity": 5}]}

    response = client.post(
        reverse("api:dispense"),
        payload,
        "application/json",
        HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_dispense__missing_id_card_no(client, snapshot, staff, material_record_factory):
    material_record_factory(location=staff.location, material__id=1)
    payload = {"material": [{"id": 1, "quantity": 5}]}

    response = client.post(
        reverse("api:dispense"),
        payload,
        "application/json",
        HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_dispense__zero_quantity(client, snapshot, staff, material_record_factory):
    material_record_factory(location=staff.location, material__id=1)
    payload = {"idcardno": 123456789, "material": [{"id": 1, "quantity": 0}]}

    response = client.post(
        reverse("api:dispense"),
        payload,
        "application/json",
        HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_dispense(client, snapshot, staff, material_record_factory):
    m1 = material_record_factory(
        location=staff.location, material__region=staff.location.region
    )
    m2 = material_record_factory(
        location=staff.location, material__region=staff.location.region
    )
    id_card_no = randint(0, 10 ** 11)
    payload = {
        "idcardno": id_card_no,
        "material": [
            {"id": m1.material.id, "quantity": 5},
            {"id": m2.material.id, "quantity": 10},
        ],
    }

    response = client.post(
        reverse("api:dispense"),
        payload,
        "application/json",
        HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content))
    assert Dispensed.objects.count() == 2
    assert Dispensed.objects.filter(
        material=m1.material,
        region=m1.material.region,
        location=staff.location,
        user=staff.user,
        id_card_no=id_card_no,
        quantity=5,
    ).exists()
    assert Dispensed.objects.filter(
        material=m2.material,
        region=m2.material.region,
        location=staff.location,
        user=staff.user,
        id_card_no=id_card_no,
        quantity=10,
    ).exists()


def test_validate__full_limit(client, snapshot, material_record_factory, staff):
    material_record_factory(
        location=staff.location,
        material__id=1,
        material__limit=10,
        material__period=5,
        material__name="Respirátor",
    )
    material_record_factory(
        location=staff.location,
        material__id=2,
        material__limit=2,
        material__period=7,
        material__name="Rouška",
    )
    material_record_factory(material__id=3)
    payload = {"idcardno": randint(0, 10 ** 11)}

    response = client.post(
        reverse("api:validate"),
        payload,
        "application/json",
        HTTP_AUTHORIZATION=staff.api_token.header,
    )

    assert response.status_code == 200
    snapshot.assert_match(json.loads(response.content))
