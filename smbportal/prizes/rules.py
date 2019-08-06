#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Permissions for accessing prize related resources and info

These permissions are kept in memory, they do not need to be stored in the db

"""

import logging

import rules

from profiles import rules as profile_rules

logger = logging.getLogger(__name__)

is_competition_moderator = rules.is_group_member("competition_moderators")

rules.add_perm("prizes", is_competition_moderator)

for perm, predicate in {
    "can_list_competitions": profile_rules.is_privileged_user,
    "can_list_own_competitions": profile_rules.is_end_user,
    "view_sponsor": is_competition_moderator,
    "add_sponsor": is_competition_moderator,
    "change_sponsor": is_competition_moderator,
    "view_competition": is_competition_moderator,
    "add_prize": is_competition_moderator,
    "change_prize": is_competition_moderator,
    "view_prize": is_competition_moderator,
    "add_competition": is_competition_moderator,
    "change_competition": is_competition_moderator,
    "view_pendingcompetitionparticipant": is_competition_moderator,
    "change_pendingcompetitionparticipant": is_competition_moderator,
    "view_competitionparticipant": is_competition_moderator,
    "change_competitionparticipant": is_competition_moderator,
}.items():
    rules.add_perm("prizes.{}".format(perm), predicate)
