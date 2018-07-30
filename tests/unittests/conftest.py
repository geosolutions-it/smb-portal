from unittest import mock

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture(scope="session")
def api_request_factory():
    factory = APIRequestFactory()
    return factory


@pytest.fixture
def mocked_user():
    mocked_user_class = mock.MagicMock(
        spec="api.serializers.profiles.models.SmbUser")
    return mocked_user_class()
