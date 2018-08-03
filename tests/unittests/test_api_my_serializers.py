#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import pytest

from api import serializers

pytestmark = pytest.mark.unit


def test_myuserserializer_returns_my_url(mocked_end_user):
    serializer = serializers.MyUserSerializer(
        instance=mocked_end_user,
        context={
            "request": None
        }
    )
    assert serializer.data["url"] == "/api/my-user"


def test_myphysicaltagserializer_returns_my_urls(mocked_tag):
    serializer = serializers.MyPhysicalTagSerializer(
        instance=mocked_tag, context={"request": None}
    )
    assert serializer.data["url"].startswith("/api/my-tags")
    assert serializer.data["bike_url"].startswith("/api/my-bikes")
