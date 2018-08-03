from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory

import profiles.models


@pytest.fixture(scope="session")
def api_request_factory():
    factory = APIRequestFactory()
    return factory


@pytest.fixture
def mocked_user():
    mocked_user_class = mock.MagicMock(
        spec="api.serializers.profiles.models.SmbUser")
    return mocked_user_class()


@pytest.fixture
def mocked_end_user(mocked_user, settings):
    # this mock is created from an instance in order to make sure the mock
    # is able to pass isinstance tests. For more info see:
    # http://www.voidspace.org.uk/python/mock/mock.html#the-mock-class
    # mocked_end_user_class = mock.MagicMock(
    #     spec="profiles.models.EndUserProfile"
    # )
    mocked_group_class = mock.MagicMock(
        spec="django.contrib.auth.models.Group")
    mocked_group = mocked_group_class()
    mocked_group.name = settings.END_USER_PROFILE
    mocked_end_user_profile = mock.MagicMock(
        spec=profiles.models.EndUserProfile(),
        user=mocked_user
    )
    mocked_user.enduserprofile = mocked_end_user_profile
    mocked_user.profile = mocked_end_user_profile
    mocked_user.groups.return_value = [
        mocked_group,
    ]
    mocked_user.keycloak.return_value = mock.MagicMock(
        spec="bossoidc.models.Keycloak")
    mocked_user.keycloak.UID = "fake_uuid"
    mocked_user.email = "fake.mail@mail.com"
    mocked_user.usename = "fake"
    return mocked_user


@pytest.fixture
def mocked_tag(mocked_bike):
    mocked_tag_class = mock.MagicMock(spec="vehicles.models.PhysicalTag")
    mocked_tag = mocked_tag_class()
    mocked_tag.bike = mocked_bike
    mocked_tag.epc = "mocked-epc-123"
    return mocked_tag
