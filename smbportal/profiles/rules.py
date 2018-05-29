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


is_end_user = rules.is_group_member("end_users")

rules.add_perm("profiles.can_create", ~has_profile)
rules.add_perm("profiles.can_view", has_profile & is_profile_owner)
rules.add_perm("profiles.can_edit", has_profile & is_profile_owner)
