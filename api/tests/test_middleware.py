import json

import pytest

from ..middleware import ApiTokenAuthMiddleware

pytestmark = pytest.mark.django_db


@pytest.fixture
def token_middleware():
    return ApiTokenAuthMiddleware(lambda r: r)


@pytest.fixture
def request_factory(mocker, settings):
    def factory(header=None, user=None, path_info=None, get=None):
        request = mocker.Mock()
        request.user = user
        request.path_info = f"/{settings.API_URL}" if path_info is None else path_info
        request.META.get.return_value = header
        request.GET = {} if get is None else get
        return request

    return factory


def test_not_api_path(request_factory, token_middleware):
    request = request_factory(path_info="/random/")

    response = token_middleware(request)

    request.META.get.assert_not_called()
    assert response == request


def test_no_auth_header_no_url(request_factory, token_middleware):
    request = request_factory()

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response == request
    assert response.user is None


def test_wrong_auth_header(request_factory, token_middleware, api_token, snapshot):
    request = request_factory(header=f"Token {api_token.token}")

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_auth_header_with_invalid_token(request_factory, token_middleware, snapshot):
    request = request_factory(header=f"Bearer WRONG")

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_auth_header_with_valid_token(request_factory, token_middleware, api_token):
    request = request_factory(header=f"Bearer {api_token.token}")

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response == request
    assert response.user == api_token.user


def test_url_param_with_invalid_token(request_factory, token_middleware, snapshot):
    request = request_factory(get={"token": "wrong"})

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_url_param_with_valid_token(
    request_factory, token_middleware, api_token, snapshot
):
    request = request_factory(get={"token": api_token.token})

    response = token_middleware(request)

    request.META.get.assert_called_once_with("HTTP_AUTHORIZATION")
    assert response == request
    assert response.user == api_token.user
