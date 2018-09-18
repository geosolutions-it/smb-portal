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
from django.utils.translation import ugettext_lazy as _

import django_gamification.models as gm


# NOTE: Badge points are used for unlockables, which we are not using here
CATEGORIES = {
    "user_registration": {
        "name": _("user_registration"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("new_user"),
                "description": _(
                    "As soon as you sign up and install the APP you earn "
                    "this badge."
                ),
                "progression_target": 0,  # this badge is awarded immediately
            },
        ]
    },
    "data_collection": {
        "name": _("data_collection"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("data_collector_level0"),
                "description": _(
                    "When you start entering the tracking data of your "
                    "transport modes, you get this badge."
                ),
                "progression_target": 0,  # this badge is awarded immediately
            },
            {
                "name": _("data_collector_level1"),
                "description": _(
                    "When you have recorded activity in a week for each day, "
                    "you will get this badge."
                ),
                "progression_target": 7,
            },
            {
                "name": _("data_collector_level2"),
                "description": _(
                    "When you have recorded activity in two weeks for each "
                    "day, you will get this badge."
                ),
                "progression_target": 14,
            },
            {
                "name": _("data_collector_level3"),
                "description": _(
                    "When you have recorded activity in a month for each day, "
                    "you will get this badge."
                ),
                "progression_target": 30,
            },

        ]
    },
    "bike_usage": {
        "name": _("bike_usage"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("biker_level1"),
                "description": _(
                    "Start using your bike in the city! Use the bike three "
                    "times in a week and you will get this badge."
                ),
                "progression_target": 3,
            },
            {
                "name": _("biker_level2"),
                "description": _(
                    "Reuse the bike three more times in the city in the next "
                    "week and you will get this badge."
                ),
                "progression_target": 6,
            },
            {
                "name": _("biker_level3"),
                "description": _(
                    "Reuse the bike in the city another six times in the "
                    "next two weeks and you will get this badge!!"
                ),
                "progression_target": 12,
            },
            {
                "name": _("bike_surfer_level1"),
                "description": _(
                    "Use the bike for at least 10 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 10,
            },
            {
                "name": _("bike_surfer_level2"),
                "description": _(
                    "Use the bike for at least 50 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 50,
            },
            {
                "name": _("bike_surfer_level3"),
                "description": _(
                    "Use the bike for at least 100 km in urban areas and "
                    "you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 100,
            },
        ]
    },
    "public_transport_usage": {
        "name": _("public_transport_usage"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("public_mobility_level1"),
                "description": _(
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On first use of public transport you will "
                    "get this badge."
                ),
                "progression_target": 1,
            },
            {
                "name": _("public_mobility_level2"),
                "description": _(
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On the fifth use of public transport you "
                    "will get this badge."
                ),
                "progression_target": 5,
            },
            {
                "name": _("public_mobility_level3"),
                "description": _(
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On the tenth use of public transport you "
                    "will get this badge."
                ),
                "progression_target": 10,
            },
            {
                "name": _("tpl_surfer_level1"),
                "description": _(
                    "Use the bus for at least 25 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 25,
            },
            {
                "name": _("tpl_surfer_level2"),
                "description": _(
                    "Use the bus for at least 100 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 100,
            },
            {
                "name": _("tpl_surfer_level3"),
                "description": _(
                    "Use the bus for at least 200 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 200,
            },
        ]
    },
    "sustainability": {
        "name": _("sustainability"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("multi_surfer_level1"),
                "description": _(
                    "Use sustainable means for at least 100 km in urban "
                    "areas and you will get this badge! You have made a "
                    "great contribution to sustainable mobility in your city!"
                ),
                "progression_target": 100,
            },
            {
                "name": _("multi_surfer_level2"),
                "description": _(
                    "Use sustainable means for at least 250 km in urban areas "
                    "and you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 250,
            },
            {
                "name": _("multi_surfer_level3"),
                "description": _(
                    "Use sustainable means for at least 500 km in urban areas "
                    "and you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 500,
            },
            {
                "name": _("ecologist_level1"),
                "description": _(
                    "Avoid emissions for 25 kg of CO2 in urban areas and you "
                    "will get this badge!"
                ),
                "progression_target": 25,
            },
            {
                "name": _("ecologist_level2"),
                "description": _(
                    "Avoid emissions for 50 kg of CO2 in urban areas and you "
                    "will get this badge!"
                ),
                "progression_target": 50,
            },
            {
                "name": _("ecologist_level3"),
                "description": _(
                    "Avoid emissions for 100 kg of CO2 in urban areas and "
                    "you will get this badge!"
                ),
                "progression_target": 100,
            },

        ]
    },
    "health_benefits": {
        "name": _("health_benefits"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("healthy_level1"),
                "description": _(
                    'Consume a total of 750 calories thanks to your movements '
                    '"active" in urban areas and you will get this badge!'
                ),
                "progression_target": 750,
            },
            {
                "name": _("healthy_level2"),
                "description": _(
                    'Consume a total of 2250 calories thanks to your '
                    'movements "active" in urban areas and you will get this '
                    'badge!'
                ),
                "progression_target": 2250,
            },
            {
                "name": _("healthy_level3"),
                "description": _(
                    'Consume a total of 4500 calories thanks to your '
                    'movements "active" in urban areas and you will get this '
                    'badge!'
                ),
                "progression_target": 4500,
            },
        ]
    },
    "cost_savings": {
        "name": _("cost_savings"),
        "description": _(""),
        "badge_definitions": [
            {
                "name": _("money_saver_level1"),
                "description": _(
                    "Save a total of 6 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 6,
            },
            {
                "name": _("money_saver_level2"),
                "description": _(
                    "Save a total of 12 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 12,
            },
            {
                "name": _("money_saver_level3"),
                "description": _(
                    "Save a total of 24 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 24,
            },
        ]
    },
}


class Command(BaseCommand):
    help = "Generate the default badge definitions for smb portal"

    def handle(self, *args, **options):
        for cat_name, cat_config in CATEGORIES.items():
            self.generate_category(**cat_config)
        self.stdout.write("Done!")

    def generate_category(self, name="", description="",
                          badge_definitions=None, **kwargs):
        category, created = gm.Category.objects.get_or_create(
            name=name,
            description=description
        )
        for definition in badge_definitions or []:
            badge_def, created = gm.BadgeDefinition.objects.get_or_create(
                name=definition["name"],
                description=definition["description"],
                points=definition.get("points"),
                progression_target=definition.get("progression_target"),
                category=category,
            )
            if created:
                self.stdout.write(
                    "Created badge definition {}".format(badge_def.name))
