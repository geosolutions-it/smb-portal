#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Constants used for calculating segment data"""

from tracks import models

SO2 = {
    "unit": "mg/km",
    models.CAR: 1.1,
    models.BUS: 4.4,
    models.SCOOTER: 0.3,
    models.MOTORBIKE: 0.6,
}

NOX = {
    "unit": "mg/km",
    models.CAR: 460,
    models.BUS: 6441,
    models.SCOOTER: 158,
    models.MOTORBIKE: 165,
}

CO = {
    "unit": "mg/km",
    models.CAR: 617,
    models.BUS: 1451,
    models.SCOOTER: 5282,
    models.MOTORBIKE: 6505,
}

CO2 = {
    "unit": "g/km",
    models.CAR: 177,
    models.BUS: 668,
    models.SCOOTER: 49,
    models.MOTORBIKE: 100,
}

PM10 = {
    "unit": "mg/km",
    models.CAR: 46,
    models.BUS: 273,
    models.SCOOTER: 96,
    models.MOTORBIKE: 34,
}

FUEL_PRICE = {
    "unit": "eur/l",
    models.BUS: 1,
    models.CAR: 1,
    models.MOTORBIKE: 0.8,
    models.SCOOTER: 0.8,
}

FUEL_CONSUMPTION = {
    "unit": "km/l",
    models.BUS: 3,
    models.CAR: 11.5,
    models.MOTORBIKE: 20,
    models.SCOOTER: 30,
}

TIME_COST_PER_HOUR_EURO = 8

DEPRECIATION_COST = {
    "unit": "euro/km",
    models.BUS: 0,
    models.CAR: 0.106,
    models.MOTORBIKE: 0.111,
    models.SCOOTER: 0.089,
}

OPERATION_COST = {
    "unit": "euro/km",
    models.BUS: 0,
    models.CAR: 0.072,
    models.MOTORBIKE: 0.058,
    models.SCOOTER: 0.162,
}

CALORY_CONSUMPTION = {
    "unit": "cal/minute",
    models.FOOT: {
        "unit": "km/h",
        "steps": [
            {"speed": 5.5, "calories": 5.28},
            {"speed": 6.5, "calories": 5.94},
        ],
    },
    models.BIKE: {
        "unit": "km/h",
        "steps": [
            {"speed": 13, "calories": 4.87},
            {"speed": 19, "calories": 7.03},
            {"speed": 24, "calories": 9.26},
            {"speed": 27, "calories": 11.14},
            {"speed": 30, "calories": 13.38},
        ],
    },
}

HEALTH_BENEFIT_INDEX = {
    models.FOOT: {
        "applicable_age": (20, 74),
        "relatve_risk": 0.883,
        "threshold": (146, "hours/year"),
        "maximum_percentage": 0.3
    },
    models.BIKE: {
        "applicable_age": (20, 64),
        "relatve_risk": 0.899,
        "threshold": (87, "hours/year"),
        "maximum_percentage": 0.45
    },
}
