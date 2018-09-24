#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import re

from django.core.management.base import BaseCommand

import django_gamification.models as gm

from badges import  utils
from badges.constants import CATEGORIES
import profiles.models as pm


class Command(BaseCommand):
    help = "Generate the default badge definitions for smb portal"

    def handle(self, *args, **options):
        self.stdout.write(
            "Deleting any previous gamification features...")
        self.drop_previous_gamification_interfaces()
        self.drop_previous_badge_definitions()
        self.stdout.write("Adding gamification interface to endusers...")
        self.add_user_gamification_interfaces()
        self.stdout.write("Generating badge definitions and badges...")
        self.generate_categories(CATEGORIES)
        self.generate_badge_definitions(CATEGORIES)
        self.stdout.write("Awarding `new user` badge for existing users...")
        self.award_new_user_badges()
        self.stdout.write("Done!")

    def drop_previous_gamification_interfaces(self):
        gm.GamificationInterface.objects.all().delete()

    def drop_previous_badge_definitions(self):
        gm.BadgeDefinition.objects.all().delete()

    def add_user_gamification_interfaces(self):
        for enduser_profile in pm.EndUserProfile.objects.all():
            user = enduser_profile.user
            utils.add_gamification_interface(user)

    def generate_badge_definitions(self, category_definitions):
        defs = []
        for category_info in category_definitions:
            for badge_info in category_info["badge_definitions"]:
                info = badge_info.copy()
                info["category"] = gm.Category.objects.get(
                    name=category_info["name"])
                defs.append(info)
        ordered_defs = sort_badge_definitions(defs)
        for badge_definition in reversed(ordered_defs):
            next_name = badge_definition.get("next")
            if next_name is not None:
                next_badge = gm.BadgeDefinition.objects.get(name=next_name)
            else:
                next_badge = None
            gm.BadgeDefinition.objects.create(
                name=badge_definition["name"],
                description=badge_definition["description"],
                points=badge_definition.get("points"),
                progression_target=badge_definition.get("progression_target"),
                category=badge_definition["category"],
                next_badge=next_badge
            )

    def generate_categories(self, category_definitions):
        for category_info in category_definitions:
            gm.Category.objects.get_or_create(
                name=category_info["name"],
                description=category_info["description"]
            )

    def award_new_user_badges(self):
        for enduser_profile in pm.EndUserProfile.objects.all():
            user = enduser_profile.user
            utils.award_new_user_badge(user)


def sort_badge_definitions(items, regexp="(\d+)"):
    return sorted(
        items,
        key=lambda item: [int(c) if c.isdigit() else c for
                          c in re.split(regexp, item["name"])]
    )

