#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""utillity functions for working with badges"""

import django_gamification.models as gm

from .constants import CATEGORIES


def add_gamification_interface(user):
    if user.gamification_interface is None:
        gi = gm.GamificationInterface.objects.create()
        user.gamification_interface = gi
        user.save()


def award_new_user_badge(user):
    interface = user.gamification_interface
    new_user_badge = interface.badge_set.get(
        name=CATEGORIES[
            "user_registration"]["badge_definitions"][0]["name"])
    if not new_user_badge.acquired:
        new_user_badge.award()
        new_user_badge.save()
