import json

import pytest
from django.urls import reverse
from faker import Faker

from main.models import LocationStaff

pytestmark = pytest.mark.django_db

fake = Faker()


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


def test_login__staff_admin(client, snapshot, location_staff_factory):
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


def test_login__staff_volunteer(client, snapshot, location_staff_factory):
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
