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

from enum import Enum


class VehicleType(Enum):
    foot = 1
    bike = 2
    bus = 3
    car = 4
    scooter = 5
    motorbike = 6
    average_motorbike = 7
    unknown = 8


def _get_average(*args):
    return sum(args) / len(args)


SO2 = {
    "unit": "mg/km",
    VehicleType.car: 1.1,
    VehicleType.bus: 4.4,
    VehicleType.scooter: 0.3,
    VehicleType.motorbike: 0.6,
}
SO2[VehicleType.average_motorbike] = _get_average(
    SO2[VehicleType.scooter], SO2[VehicleType.motorbike])

NOX = {
    "unit": "mg/km",
    VehicleType.car: 460,
    VehicleType.bus: 6441,
    VehicleType.scooter: 158,
    VehicleType.motorbike: 165,
}
NOX[VehicleType.average_motorbike] = _get_average(
    NOX[VehicleType.scooter], NOX[VehicleType.motorbike])

CO = {
    "unit": "mg/km",
    VehicleType.car: 617,
    VehicleType.bus: 1451,
    VehicleType.scooter: 5282,
    VehicleType.motorbike: 6505,
}
CO[VehicleType.average_motorbike] = _get_average(
    CO[VehicleType.scooter], CO[VehicleType.motorbike])

CO2 = {
    "unit": "g/km",
    VehicleType.car: 177,
    VehicleType.bus: 668,
    VehicleType.scooter: 49,
    VehicleType.motorbike: 100,
}
CO2[VehicleType.average_motorbike] = _get_average(
    CO2[VehicleType.scooter], CO2[VehicleType.motorbike])

PM10 = {
    "unit": "mg/km",
    VehicleType.car: 46,
    VehicleType.bus: 273,
    VehicleType.scooter: 96,
    VehicleType.motorbike: 34,
}
PM10[VehicleType.average_motorbike] = _get_average(
    PM10[VehicleType.scooter], PM10[VehicleType.motorbike])

FUEL_PRICE = {
    "unit": "eur/l",
    VehicleType.bus: 1,
    VehicleType.car: 1,
    VehicleType.motorbike: 0.8,
    VehicleType.scooter: 0.8,
}
FUEL_PRICE[VehicleType.average_motorbike] = _get_average(
    FUEL_PRICE[VehicleType.scooter], FUEL_PRICE[VehicleType.motorbike])

FUEL_CONSUMPTION = {
    "unit": "km/l",
    VehicleType.bus: 3,
    VehicleType.car: 11.5,
    VehicleType.motorbike: 20,
    VehicleType.scooter: 30,
}
FUEL_CONSUMPTION[VehicleType.average_motorbike] = _get_average(
    FUEL_CONSUMPTION[VehicleType.scooter],
    FUEL_CONSUMPTION[VehicleType.motorbike]
)

TIME_COST_PER_HOUR_EURO = 8

DEPRECIATION_COST = {
    "unit": "euro/km",
    VehicleType.bus: 0,
    VehicleType.car: 0.106,
    VehicleType.motorbike: 0.111,
    VehicleType.scooter: 0.089,
}
DEPRECIATION_COST[VehicleType.average_motorbike] = _get_average(
    DEPRECIATION_COST[VehicleType.scooter],
    DEPRECIATION_COST[VehicleType.motorbike]
)

OPERATION_COST = {
    "unit": "euro/km",
    VehicleType.bus: 0,
    VehicleType.car: 0.072,
    VehicleType.motorbike: 0.058,
    VehicleType.scooter: 0.162,
}
OPERATION_COST[VehicleType.average_motorbike] = _get_average(
    OPERATION_COST[VehicleType.scooter],
    OPERATION_COST[VehicleType.motorbike]
)

CALORY_CONSUMPTION = {
    "unit": "cal/minute",
    VehicleType.foot: {
        "unit": "km/h",
        "steps": [
            {"speed": 5.5, "calories": 5.28},
            {"speed": 6.5, "calories": 5.94},
        ],
    },
    VehicleType.bike: {
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
    VehicleType.foot: {
        "applicable_age": (20, 74),
        "relatve_risk": 0.883,
        "threshold": (146, "hours/year"),
        "maximum_percentage": 0.3
    },
    VehicleType.bike: {
        "applicable_age": (20, 64),
        "relatve_risk": 0.899,
        "threshold": (87, "hours/year"),
        "maximum_percentage": 0.45
    },
}
