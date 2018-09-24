#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

NEW_USER_BADGE = "01_new_user"

# NOTE: Badge points are used for unlockables, which we are not using here
CATEGORIES = [
    {
        "name": "user_registration",
        "description": "",
        "badge_definitions": [
            {
                "name": NEW_USER_BADGE,
                "description": (
                    "As soon as you sign up and install the APP you earn "
                    "this badge."
                )
                ,
                "progression_target": 0,  # this badge is awarded immediately
            },
        ]
    },
    {
        "name": "data_collection_frequency",
        "description": "",
        "badge_definitions": [
            {
                "name": "02_data_collector_level0",
                "description": (
                    "When you start entering the tracking data of your "
                    "transport modes, you get this badge."
                ),
                "progression_target": 1,
                "next": "03_data_collector_level1",
            },
            {
                "name": "03_data_collector_level1",
                "description": (
                    "When you have recorded activity in a week for each day, "
                    "you will get this badge."
                ),
                "progression_target": 7,
                "next": "04_data_collector_level2",
            },
            {
                "name": "04_data_collector_level2",
                "description": (
                    "When you have recorded activity in two weeks for each "
                    "day, you will get this badge."
                ),
                "progression_target": 14,
                "next": "05_data_collector_level3",
            },
            {
                "name": "05_data_collector_level3",
                "description": (
                    "When you have recorded activity in a month for each day, "
                    "you will get this badge."
                ),
                "progression_target": 30,
            },

        ]
    },
    {
        "name": "bike_usage_frequency",
        "description": "",
        "badge_definitions": [
            {
                "name": "06_biker_level1",
                "description": (
                    "Start using your bike in the city! Use the bike three "
                    "times in a week and you will get this badge."
                ),
                "progression_target": 3,
                "next": "07_biker_level2",
            },
            {
                "name": "07_biker_level2",
                "description": (
                    "Reuse the bike three more times in the city in the next "
                    "week and you will get this badge."
                ),
                "progression_target": 6,
                "next": "08_biker_level3",
            },
            {
                "name": "08_biker_level3",
                "description": (
                    "Reuse the bike in the city another six times in the "
                    "next two weeks and you will get this badge!!"
                ),
                "progression_target": 12,
            },
        ]
    },
    {
        "name": "bike_travel",
        "description": "",
        "badge_definitions": [
            {
                "name": "12_bike_surfer_level1",
                "description": (
                    "Use the bike for at least 10 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 10,
                "next": "13_bike_surfer_level2",
            },
            {
                "name": "13_bike_surfer_level2",
                "description": (
                    "Use the bike for at least 50 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 50,
                "next": "14_bike_surfer_level3",
            },
            {
                "name": "14_bike_surfer_level3",
                "description": (
                    "Use the bike for at least 100 km in urban areas and "
                    "you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 100,
            },
        ]
    },
    {
        "name": "public_transport_usage_frequency",
        "description": "",
        "badge_definitions": [
            {
                "name": "09_public_mobility_level1",
                "description": (
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On first use of public transport you will "
                    "get this badge."
                ),
                "progression_target": 1,
                "next": "10_public_mobility_level2",
            },
            {
                "name": "10_public_mobility_level2",
                "description": (
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On the fifth use of public transport you "
                    "will get this badge."
                ),
                "progression_target": 5,
                "next": "11_public_mobility_level3",
            },
            {
                "name": "11_public_mobility_level3",
                "description": (
                    "Block your car and use urban public transport (tram, "
                    "bus, metro)! On the tenth use of public transport you "
                    "will get this badge."
                ),
                "progression_target": 10,
            }
        ]
    },
    {
        "name": "bus_travel",
        "description": "",
        "badge_definitions": [
            {
                "name": "15_tpl_surfer_level1",
                "description": (
                    "Use the bus for at least 25 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 25,
                "next": "16_tpl_surfer_level2",
            },
            {
                "name": "16_tpl_surfer_level2",
                "description": (
                    "Use the bus for at least 100 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 100,
                "next": "17_tpl_surfer_level3",
            },
            {
                "name": "17_tpl_surfer_level3",
                "description": (
                    "Use the bus for at least 200 km in urban areas and you "
                    "will get this badge! You have made a great contribution "
                    "to sustainable mobility in your city!"
                ),
                "progression_target": 200,
            },
        ]
    },
    {
        "name": "sustainable_travel",
        "description": "",
        "badge_definitions": [
            {
                "name": "18_multi_surfer_level1",
                "description": (
                    "Use sustainable means for at least 100 km in urban "
                    "areas and you will get this badge! You have made a "
                    "great contribution to sustainable mobility in your city!"
                ),
                "progression_target": 100,
                "next": "19_multi_surfer_level2",
            },
            {
                "name": "19_multi_surfer_level2",
                "description": (
                    "Use sustainable means for at least 250 km in urban areas "
                    "and you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 250,
                "next": "20_multi_surfer_level3",
            },
            {
                "name": "20_multi_surfer_level3",
                "description": (
                    "Use sustainable means for at least 500 km in urban areas "
                    "and you will get this badge! You have made a great "
                    "contribution to sustainable mobility in your city!"
                ),
                "progression_target": 500,
            }
        ]
    },
    {
        "name": "avoid_co2",
        "description": "",
        "badge_definitions": [
            {
                "name": "21_ecologist_level1",
                "description": (
                    "Avoid emissions for 25 kg of CO2 in urban areas and you "
                    "will get this badge!"
                ),
                "progression_target": 25,
                "next": "22_ecologist_level2",
            },
            {
                "name": "22_ecologist_level2",
                "description": (
                    "Avoid emissions for 50 kg of CO2 in urban areas and you "
                    "will get this badge!"
                ),
                "progression_target": 50,
                "next": "23_ecologist_level3",
            },
            {
                "name": "23_ecologist_level3",
                "description": (
                    "Avoid emissions for 100 kg of CO2 in urban areas and "
                    "you will get this badge!"
                ),
                "progression_target": 100,
            },

        ]
    },
    {
        "name": "health_benefit",
        "description": "",
        "badge_definitions": [
            {
                "name": "24_healthy_level1",
                "description": (
                    'Consume a total of 750 calories thanks to your movements '
                    '"active" in urban areas and you will get this badge!'
                ),
                "progression_target": 750,
                "next": "25_healthy_level2",
            },
            {
                "name": "25_healthy_level2",
                "description": (
                    'Consume a total of 2250 calories thanks to your '
                    'movements "active" in urban areas and you will get this '
                    'badge!'
                ),
                "progression_target": 2250,
                "next": "26_healthy_level3",
            },
            {
                "name": "26_healthy_level3",
                "description": (
                    'Consume a total of 4500 calories thanks to your '
                    'movements "active" in urban areas and you will get this '
                    'badge!'
                ),
                "progression_target": 4500,
            },
        ]
    },
    {
        "name": "cost_savings",
        "description": "",
        "badge_definitions": [
            {
                "name": "27_money_saver_level1",
                "description": (
                    "Save a total of 6 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 6,
                "next": "28_money_saver_level2",
            },
            {
                "name": "28_money_saver_level2",
                "description": (
                    "Save a total of 12 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 12,
                "next": "29_money_saver_level3",
            },
            {
                "name": "29_money_saver_level3",
                "description": (
                    "Save a total of 24 € thanks to your sustainable travel "
                    "in urban areas and you will get this badge!"
                ),
                "progression_target": 24,
            },
        ]
    },
]

