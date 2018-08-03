import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        "--url",
    )
    parser.addoption(
        "--keycloak-base-url",
    )
    parser.addoption(
        "--keycloak-realm",
    )
    parser.addoption(
        "--keycloak-client-id",
    )
    parser.addoption(
        "--keycloak-admin",
    )
    parser.addoption(
        "--keycloak-password",
    )


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def keycloak_base_url(request):
    return request.config.getoption("--keycloak-base-url")


@pytest.fixture
def keycloak_realm(request):
    return request.config.getoption("--keycloak-realm")


@pytest.fixture
def keycloak_client_id(request):
    return request.config.getoption("--keycloak-client-id")


@pytest.fixture
def keycloak_admin(request):
    return request.config.getoption("--keycloak-admin")


@pytest.fixture
def keycloak_password(request):
    return request.config.getoption("--keycloak-password")


@pytest.fixture()
def access_token(keycloak_base_url, keycloak_realm, keycloak_client_id,
                 keycloak_admin, keycloak_password):
    token_url = "{}/auth/realms/{}/protocol/openid-connect/token".format(
        keycloak_base_url, keycloak_realm)
    response = requests.post(
        token_url,
        data={
            "client_id": keycloak_client_id,
            "grant_type": "password",
            "username": keycloak_admin,
            "password": keycloak_password,
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]
