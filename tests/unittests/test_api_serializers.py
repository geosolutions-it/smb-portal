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

from bossoidc.models import Keycloak
from rest_framework.reverse import reverse
import pytest

from api import serializers

pytestmark = pytest.mark.unit


def test_smbuserhyperlinkedidentityfield_returns_uuid(api_request_factory,
                                                      mocked_user):
    fake_uuid = "fake_uuid"
    fake_request = api_request_factory.get(
        reverse("api:users-detail", kwargs={"uuid": fake_uuid}))
    user_detail_view_name = "api:users-detail"
    field = serializers.SmbUserHyperlinkedIdentityField(
        view_name=user_detail_view_name,
        read_only=True
    )
    mocked_user.keycloak.return_value = mock.MagicMock(spec=Keycloak)
    mocked_user.keycloak.UID = fake_uuid
    result = field.get_url(
        mocked_user,
        view_name=user_detail_view_name,
        request=fake_request,
        format=None
    )
    assert result.endswith("{}/".format(fake_uuid))


def test_smbuserhyperlinkedrelatedfield_returns_uuid(api_request_factory,
                                                     mocked_user):
    fake_uuid = "fake_uuid"
    fake_request = api_request_factory.get(
        reverse("api:bikes-detail", kwargs={"short_uuid": "phony"}))
    user_detail_view_name = "api:users-detail"
    field = serializers.SmbUserHyperlinkedRelatedField(
        view_name=user_detail_view_name,
        read_only=True
    )
    mocked_user.keycloak.return_value = mock.MagicMock(spec=Keycloak)
    mocked_user.keycloak.UID = fake_uuid
    result = field.get_url(
        mocked_user,
        view_name=user_detail_view_name,
        request=fake_request,
        format=None
    )
    assert result.endswith("{}/".format(fake_uuid))


def test_smbuserserializer_returns_uuid(api_request_factory, mocked_user):
    """verify that SmbUserSerializer returns the correct id data

    SmbUserSerializer should show ``id`` as being the keycloak UUID. Django
    identifier must be kept private

    """

    fake_uuid = "fake uuid"
    fake_request = api_request_factory.get(
        reverse("api:users-detail", kwargs={"uuid": fake_uuid}))
    mocked_user.keycloak.return_value = mock.MagicMock(spec=Keycloak)
    mocked_user.keycloak.UID = fake_uuid
    mocked_user.profile = None
    serializer = serializers.SmbUserSerializer(
        instance=mocked_user,
        context={"request": fake_request}
    )
    serializer_data = serializer.data
    assert serializer_data["uuid"] == fake_uuid
