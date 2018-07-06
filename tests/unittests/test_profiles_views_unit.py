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
from unittest import mock

from keycloakauth.keycloakadmin import KeycloakManager
from profiles import views

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("current_groups,to_enforce,expected_missing", [
    ([], ["group1"], ["group1"]),
    ([], ["group1", "group2"], ["group1", "group2"]),
    (["group1"], ["group1", "group2"], ["group2"]),
    (["group1"], [], []),
])
@mock.patch("profiles.views.get_keycloak_manager", autospec=True)
def test_enforce_keycloak_group_memberships(mock_get_manager,
                                            current_groups,
                                            to_enforce,
                                            expected_missing,
                                            settings):
    user_id = "something"
    user_profile = "other"
    settings.KEYCLOAK = {
        "group_mappings": {
            user_profile: to_enforce,
        },
        "base_url": "nowhere",
        "realm": "no realm",
        "client_id": "bogus",
        "admin_username": "fake_user",
        "admin_password": "fake_password",
    }
    settings.END_USER_PROFILE = user_profile
    fake_manager = mock.MagicMock(spec=KeycloakManager)
    mock_get_manager.return_value = fake_manager
    expected_calls = []
    for missing in expected_missing:
        expected_calls.append(mock.call(user_id, missing))
    result = views.enforce_keycloak_group_memberships(
        user_id, user_profile, current_groups)
    fake_manager.add_user_to_group.assert_has_calls(
        expected_calls, any_order=True)
    assert result == to_enforce
