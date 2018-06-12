#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Unit tests for the keycloakauth.permissions module"""

from django.contrib.auth.models import Group

import pytest

import keycloakauth.permissions

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("perms, expected", [
    (("list_stuff",), ["list_stuff",]),
    (("create_stuff",), []),
    (("create_stuff", "list_stuff"), ["list_stuff"]),
    (("new_stuff",), []),
    (("new_stuff", "list_stuff"), ["list_stuff"]),
    (("edit_stuff",), []),
    (("edit_stuff", "list_stuff"), ["list_stuff"]),
    (("update_stuff",), []),
    (("update_stuff", "list_stuff"), ["list_stuff"]),
    (("change_stuff",), []),
    (("change_stuff", "list_stuff"), ["list_stuff"]),
    (("delete_stuff",), []),
    (("delete_stuff", "list_stuff"), ["list_stuff"]),
    (("remove_stuff",), []),
    (("remove_stuff", "list_stuff"), ["list_stuff"]),
])
def test_filter_out_unsafe_permissions(perms, expected):
    result = keycloakauth.permissions.filter_out_unsafe_permissions(perms)
    assert result == expected

