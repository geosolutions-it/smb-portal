#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""pytest configuration file"""

from unittest import mock

from bossoidc.models import Keycloak
from django.contrib.auth.models import Group
import pytest
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from vehicles.models import Bike


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "unit: Run only unit tests",
    )
    config.addinivalue_line(
        "markers",
        "integration: Run only integration tests",
    )


@pytest.fixture(scope="session")
def api_request_factory():
    factory = APIRequestFactory()
    return factory


@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.logout()
    client.credentials()


@pytest.fixture
def mocked_user():
    mocked_user_class = mock.MagicMock(
        spec="api.serializers.profiles.models.SmbUser")
    return mocked_user_class()


@pytest.fixture
def privileged_user(db, django_user_model, settings):
    group = Group.objects.get_or_create(
        name=settings.PRIVILEGED_USER_PROFILE)[0]
    user = django_user_model.objects.create(username="privileged")
    group.user_set.add(user)
    group.save()
    return user


@pytest.fixture
def end_user(db, django_user_model, settings):
    group = Group.objects.get_or_create(
        name=settings.END_USER_PROFILE)[0]
    user = django_user_model.objects.create(username="enduser")
    Keycloak.objects.create(user=user, UID="keycloakuuid-abcd-123")
    group.user_set.add(user)
    group.save()
    return user


@pytest.fixture
def bike_owned_by_end_user(db, end_user):
    bike = Bike.objects.create(
        nickname="tester_bike",
        owner=end_user
    )
    return bike
