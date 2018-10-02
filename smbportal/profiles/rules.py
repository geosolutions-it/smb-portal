#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Permissions for accessing profile related resources and info

These permissions are kept in memory, they do not need to be stored in the db

"""

import logging

import rules

logger = logging.getLogger(__name__)


@rules.predicate
def is_owner(user, obj):
    return obj.owner == user


@rules.predicate
def is_profile_owner(user, profile_obj):
    return user.profile == profile_obj if user.is_authenticated else False

@rules.predicate
def has_profile(user):
    return bool(user.profile) if user.is_authenticated else False


@rules.predicate
def is_admin(user):
    return user.is_superuser


is_end_user = rules.is_group_member("end_users")
is_privileged_user = rules.is_group_member("privileged_users")

for perm, predicate in {
    "is_authenticated": rules.is_authenticated,
    "can_list_users": is_privileged_user,
    "can_delete_user": is_admin,
    "can_create_profile": ~has_profile,
    "can_view_profile": has_profile,
    "can_edit_profile": has_profile & is_profile_owner,
    "can_list_badges": is_privileged_user,
    "can_list_own_badges": is_end_user,
}.items():
    rules.add_perm("profiles.{}".format(perm), predicate)
