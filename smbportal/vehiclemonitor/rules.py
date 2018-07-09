#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Permissions for accessing vehicle observation resources and info

These permissions are kept in memory, they do not need to be stored in the db

"""

import logging

import rules

import profiles.rules

logger = logging.getLogger(__name__)

for perm, predicate in {
    "can_list_bike_observation": profiles.rules.is_privileged_user,
    "can_list_own_bike_observation": profiles.rules.is_end_user,
}.items():
    rules.add_perm("vehiclemonitor.{}".format(perm), predicate)
