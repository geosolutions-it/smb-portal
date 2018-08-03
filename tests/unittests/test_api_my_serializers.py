#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from unittest import mock

import pytest

from api import serializers
import vehicles.models

pytestmark = pytest.mark.unit


def test_myuserserializer_returns_my_url(api_request_factory, mocked_end_user):
    serializer = serializers.MyUserSerializer(
        instance=mocked_end_user,
        context={
            "request": None
        }
    )
    assert serializer.data["url"] == "/api/my-user"


def test_mybikesserializer_returns_my_urls(mocked_bike):
    serializer = serializers.MyBikeDetailSerializer(
        instance=mocked_bike,
        context={"request": None}
    )
    print("serializer.data: {}".format(serializer.data))
    assert serializer.data["owner"] == "/api/my-user"


def test_myphysicaltagserializer_returns_my_urls(mocked_tag):
    serializer = serializers.MyPhysicalTagSerializer(
        instance=mocked_tag, context={"request": None}
    )
    assert serializer.data["url"].startswith("/api/my-tags")
    assert serializer.data["bike_url"].startswith("/api/my-bikes")
