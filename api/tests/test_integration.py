import json
from types import SimpleNamespace

import pytest
from django.urls import reverse
from faker import Faker

from main.models import LocationStaff

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
        "login": user.username,
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
        "login": user.username,
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
        "login": ls.user.username,
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
        "login": ls.user.username,
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
        "login": ls.user.username,
        "password": password,
        "location": str(ls.location.id),
    }

    response = client.post(reverse("api:login"), payload, "application/json")

    assert response.status_code == 200
    content = json.loads(response.content)
    assert content["result"] == "success"
    assert isinstance(content["token"], str)
    assert len(content["token"]) > 50


def test_material__no_token(client, snapshot):
    response = client.get(reverse("api:material"))

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_material__not_staff(client, snapshot, api_token):
    response = client.get(reverse("api:material"), HTTP_AUTHORIZATION=api_token.header)

    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


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
