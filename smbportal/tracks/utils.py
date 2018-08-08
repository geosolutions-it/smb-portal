#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.db.models import Sum

from . import models


def get_aggregated_emissions(track_owner=None, split_by_vehicle_type=True):
    """Compute aggregated emissions


    - total emissions by type of pollutant for all users

    >>> get_aggregated_emissions(split_by_vehicle_type=False)

    - total emissions by type of pollutant and by vehicle type for all users

    >>> get_aggregated_emissions(split_by_vehicle_type=False)

    - total emissions by type of pollutant for a single user

    >>> get_aggregated_emissions(
    ...     track_owner=some_user, split_by_vehicle_type=False)

    - total emissions by type of pollutant for a single user

    - total emissions for a specific vehicle type for all users

    >>> get_aggregated_emissions().filter(segment__vehicle_type="bike").first()

    """
    qs = models.Emission.objects.values(
        "segment__vehicle_type")
    if track_owner is not None:
        qs = qs.filter(segment__track__owner=track_owner)
    qs = qs.distinct().annotate(
        so2=Sum("so2"),
        so2_saved=Sum("so2_saved"),
        nox=Sum("nox"),
        nox_saved=Sum("nox_saved"),
        co2=Sum("co2"),
        co2_saved=Sum("co2_saved"),
        co=Sum("co"),
        co_saved=Sum("co_saved"),
        pm10=Sum("pm10"),
        pm10_saved=Sum("pm10_saved"),
    )
    if not split_by_vehicle_type:
        qs = qs.aggregate(
            Sum("so2"),
            Sum("so2_saved"),
            Sum("nox"),
            Sum("nox_saved"),
            Sum("co2"),
            Sum("co2_saved"),
            Sum("co"),
            Sum("co_saved"),
            Sum("pm10"),
            Sum("pm10_saved"),
        )
    return qs
