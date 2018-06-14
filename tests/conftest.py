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

import pytest
from rest_framework.test import APIRequestFactory


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
def mocked_user():
    mocked_user_class = mock.MagicMock(
        spec="api.serializers.profiles.models.SmbUser")
    return mocked_user_class()
