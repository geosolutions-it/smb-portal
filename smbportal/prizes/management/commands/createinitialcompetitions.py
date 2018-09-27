#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import datetime as dt

from django.core.management.base import BaseCommand
import pytz

from profiles.models import EndUserProfile
from prizes.models import Competition
from prizes.models import CompetitionDefinition
import prizes.models

COMPETITION_DEFINITIONS = [
    {
        "name": "Weekly CO2 saver",
        "num_days": 7,
        "starts_at": "2018-09-02",
        "num_repeats": 157,  # ~ three years (52 weeks per year)
        "repeat": CompetitionDefinition.REPEAT_WEEKLY,
        "age_group": [
            EndUserProfile.AGE_YOUNGER_THAN_NINETEEN,
            EndUserProfile.AGE_BETWEEN_NINETEEN_AND_THIRTY,
            EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
            EndUserProfile.AGE_OLDER_THAN_SIXTY_FIVE
        ],
        "segment_by_age_group": True,
        "criteria": [
            CompetitionDefinition.CRITERIUM_SAVED_CO2_EMISSIONS,
        ],
        "winner_threshold": 1,
        "prizes": [
            {
                "name": "Some reward",
                "user_rank": 1
            }
        ]
    }
]


class Command(BaseCommand):
    help = "Generate the default competitions for smb portal"

    def handle(self, *args, **options):
        self.stdout.write(
            "Removing previous competition definitions that have the same "
            "name as the ones specified..."
        )
        remove_existing_competition_definitions(COMPETITION_DEFINITIONS)
        self.stdout.write("Creating competition definitions...")
        competition_definitions = create_competition_definitions(
            COMPETITION_DEFINITIONS)
        self.stdout.write("Creating concrete competitions...")
        for definition in competition_definitions:
            Competition.creation_manager.create_competitions(definition)


def remove_existing_competition_definitions(defs):
    qs = CompetitionDefinition.objects.filter(
        name__in=[i["name"] for i in defs])
    qs.delete()


def create_competition_definitions(defs):
    result = []
    for definition in defs:
        starts_at = dt.datetime.strptime(
            definition["starts_at"], "%Y-%m-%d").replace(tzinfo=pytz.utc)
        competition_def = CompetitionDefinition.objects.create(
            name=definition["name"],
            num_days=definition["num_days"],
            starts_at=starts_at,
            num_repeats=definition["num_repeats"],
            repeat_when=definition["repeat"],
            age_group=definition["age_group"],
            segment_by_age_group=definition["segment_by_age_group"],
            criteria=definition["criteria"],
            winner_threshold=definition["winner_threshold"]
        )
        result.append(competition_def)
        for prize_def in definition["prizes"]:
            prize, created = prizes.models.Prize.objects.get_or_create(
                name=prize_def["name"],
                description=prize_def.get("description", "")
            )
            prizes.models.CompetitionPrize.objects.get_or_create(
                prize=prize,
                competition_definition=competition_def,
                user_rank=prize_def["user_rank"]
            )
    return result
