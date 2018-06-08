#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Permissions for accessing vehicle related resources and info

These permissions are kept in memory, they do not need to be stored in the db

"""

import logging

import rules

from profiles import rules as profile_rules

logger = logging.getLogger(__name__)


@rules.predicate
def is_bike_owner(user, bike):
    return bike.owner == user


rules.add_perm("vehicles.can_list_bikes", profile_rules.is_privileged_user)
rules.add_perm("vehicles.can_create_bike", profile_rules.is_end_user)
rules.add_perm("vehicles.can_view_bike", is_bike_owner)
rules.add_perm("vehicles.can_edit_bike", is_bike_owner)

rules.add_perm(
    "vehicles.can_list_physical_tags", profile_rules.is_privileged_user)
rules.add_perm("vehicles.can_create_physical_tag", profile_rules.is_end_user)
rules.add_perm("vehicles.can_view_physical_tag", is_bike_owner)
rules.add_perm("vehicles.can_edit_physical_tag", is_bike_owner)

