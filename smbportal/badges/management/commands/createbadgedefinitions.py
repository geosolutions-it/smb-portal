#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

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
        for cat_name, cat_config in CATEGORIES.items():
            self.generate_category(**cat_config)
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

    def generate_category(self, name="", description="",
                          badge_definitions=None, **kwargs):
        category, created = gm.Category.objects.get_or_create(
            name=name,
            description=description
        )
        for definition in badge_definitions or []:
            badge_def = gm.BadgeDefinition.objects.create(
                name=definition["name"],
                description=definition["description"],
                points=definition.get("points"),
                progression_target=definition.get("progression_target"),
                category=category,
            )

    def award_new_user_badges(self):
        for enduser_profile in pm.EndUserProfile.objects.all():
            user = enduser_profile.user
            utils.award_new_user_badge(user)
