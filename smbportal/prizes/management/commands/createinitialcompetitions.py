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
import prizes.models

SPONSORS = [
    "CTTNord srl",
    "Banco di Andrea Briguglio",
    "Negozio di Roberto Sgariglia",
    "Bar Nuovo",
    "Negozio Supershoes di via del giglio",
    "Libreria 'Libri' di Daniela Barli Carboncini",
    "Torteria 'Da Gagarin'",
]

PRIZES = [  # (prize_name, sponsor_index)
    ("Abbonamento mensile BUS urbano", 0),
    ("1 kit igiene casa", 1),
    ("Buono spesa di 5 euro", 2),
    ("Colazione", 3),
    ("1 paio di ciabatte", 4),
    ("1 libro", 5),
    ("1 5& 5 e spuma", 6),
]

NAME = "Weekly CO2 saver"
CRITERIA = [Competition.CRITERIUM_SAVED_CO2_EMISSIONS]
START_DATE = "2018-09-02"
GROUP_1 = [EndUserProfile.AGE_BETWEEN_NINETEEN_AND_THIRTY]
GROUP_2 = [EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE]
GROUP_3 = [EndUserProfile.AGE_OLDER_THAN_SIXTY_FIVE]

COMPETITIONS = [
    [  # week 1
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [1],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [2],
        },
    ],
    [  # week 2
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [3],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [4],
        },
    ],
    [  # week 3
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [5],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [6],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [1],
        },
    ],
    [  # week 4
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [6],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [3],
        },
    ],
    [  # week 5
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [2],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [1],
        },
    ],
    [  # week 6
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [3],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [6],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
    ],
    [  # week 7
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [1],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [5],
        },
    ],
    [  # week 8
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [5],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [2],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [6],
        },
    ],
    [  # week 9
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [6],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [3],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [2],
        },
    ],
    [  # week 10
        {
            "name": NAME,
            "age_groups": GROUP_1,
            "criteria": CRITERIA,
            "prize_indexes": [0],
        },
        {
            "name": NAME,
            "age_groups": GROUP_2,
            "criteria": CRITERIA,
            "prize_indexes": [5],
        },
        {
            "name": NAME,
            "age_groups": GROUP_3,
            "criteria": CRITERIA,
            "prize_indexes": [4],
        },
    ],
]


class Command(BaseCommand):
    help = "Generate the default competitions for smb portal"

    def handle(self, *args, **options):
        self.stdout.write(
            "Removing previous competition definitions that have the same "
            "name as the ones specified..."
        )
        self.stdout.write("Updating sponsors...")
        update_sponsors(SPONSORS)
        self.stdout.write("Updating prizes...")
        update_prizes(PRIZES, SPONSORS)
        self.stdout.write("Removing previously existing competitions ...")
        prizes.models.Competition.objects.all().delete()
        self.stdout.write("Creating competitions ...")
        start = dt.datetime.strptime(START_DATE, "%Y-%m-%d").replace(
            tzinfo=pytz.utc)
        for index, week in enumerate(COMPETITIONS):
            self.stdout.write("Handling week {}...".format(index))
            start_date = start + dt.timedelta(days=7*index)
            end_date = start_date + dt.timedelta(days=6)
            for competition_definition in week:
                competition = prizes.models.Competition.objects.create(
                    name=NAME,
                    age_groups=competition_definition["age_groups"],
                    start_date=start_date,
                    end_date=end_date,
                    criteria=CRITERIA,
                )
                for prize_index in competition_definition["prize_indexes"]:
                    prize = prizes.models.Prize.objects.get(
                        name=PRIZES[prize_index][0])
                    prizes.models.CompetitionPrize.objects.create(
                        prize=prize,
                        competition=competition,
                        user_rank=1
                    )
        self.stdout.write("Done!")


def update_sponsors(sponsors):
    for sponsor_name in sponsors:
        prizes.models.Sponsor.objects.get_or_create(name=sponsor_name)


def update_prizes(prize_definitions, sponsor_definitions):
    for prize_name, sponsor_index in  prize_definitions:
        sponsor = prizes.models.Sponsor.objects.get(
            name=sponsor_definitions[sponsor_index])
        prizes.models.Prize.objects.get_or_create(
            name=prize_name,
            sponsor=sponsor
        )
