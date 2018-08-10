#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import random

from django.contrib.gis.db.models.functions import Length
from django.contrib.gis import geos
from django.contrib.gis.geos import MultiLineString
from django.core.management.base import BaseCommand

from tracks import models

from . import _constants


random.seed(3)


class Command(BaseCommand):
    help = (
        "Add test data for tracks. This command adds segments based on the "
        "tracks test data that is added by manage.py populatetracks. It is "
        "meant as a stop gap command while some more real test data is not "
        "available yet."
    )

    def handle(self, *args, **options):
        vehicle_types = [
            models.BIKE,
            models.BUS,
            models.FOOT,
            models.CAR,
        ]
        for track in models.Track.objects.all():
        # for track in models.Track.objects.filter(id=26):
            self.stdout.write("Processing track {}...".format(track.id))
            for vehicle_type in vehicle_types:
                self.stdout.write(
                    "Generating segments for {!r}...".format(vehicle_type))
                segments = create_segments(track, vehicle_type)
                self.stdout.write("-- Simulating emissions cost and health...")
                for segment in segments:
                    length = segment.get_length().km
                    speed = segment.get_average_speed()
                    calculate_segment_emissions(segment, length)
                    calculate_segment_cost(segment, length)
                    calculate_segment_health(segment, speed)


def create_segments(track, vehicle_type, points_per_segment=50):
    """Create segments

    This function creates segments from collected points. It employs a
    simplistic model, assuming that:

    - in the same track, each vehicle type always uses the same vehicle
    - in the same track vehicle types are used continuously, e.g. a user will
    not do bike -> bus -> bike in the same track.

    """

    qs = models.CollectedPoint.objects.filter(
        track=track,
        vehicle_type=vehicle_type,
        timestamp__isnull=False
    )
    segments = []
    track_points = qs.count()
    if track_points > 1:
        num_segments = (track_points // points_per_segment) or 1
        for segment_id in range(num_segments):
            start_index = segment_id * points_per_segment
            if segment_id == num_segments - 1:
                end_index = qs.count()
            else:
                end_index = start_index + points_per_segment
            pts = list(qs)[start_index:end_index]
            linestring = geos.LineString([pt.the_geom.coords for pt in pts])
            start = min([pt.timestamp for pt in pts])
            end = max([pt.timestamp for pt in pts])
            segment, created = models.Segment.objects.get_or_create(
                track=track,
                user_uuid=track.owner.keycloak,
                vehicle_type=vehicle_type,
                vehicle_id=pts[-1].vehicle_id,
                the_geom=MultiLineString(linestring),
                start_date=start,
                end_date=end,
            )
            segments.append(segment)
    return segments


def get_segment_length(segment_id):
    """Return length of segment, in km."""
    annotated_qs = models.Segment.objects.filter(id=segment_id).annotate(
        length=Length("the_geom", spheroid=True))
    segment_length = annotated_qs.first().length.km
    return segment_length


def calculate_segment_emissions(segment, length):
    if segment.vehicle_type not in [models.BIKE, models.FOOT]:
        emissions = _calculate_emissions(length, segment.vehicle_type)
        emissions_record = models.Emission.objects.create(
            segment=segment,
            so2=emissions["so2"],
            so2_saved=0,
            nox=emissions["nox"],
            nox_saved=0,
            co2=emissions["co2"],
            co2_saved=0,
            co=emissions["co"],
            co_saved=0,
            pm10=emissions["pm10"],
            pm10_saved=0
        )
    else:
        reference_emissions = _calculate_emissions(length, models.CAR)
        emissions_record = models.Emission.objects.create(
            segment=segment,
            so2=0,
            so2_saved=reference_emissions["so2"],
            nox=0,
            nox_saved=reference_emissions["nox"],
            co2=0,
            co2_saved=reference_emissions["co2"],
            co=0,
            co_saved=reference_emissions["co"],
            pm10=0,
            pm10_saved=reference_emissions["pm10"],
        )
    return emissions_record


def calculate_segment_cost(segment, length):
    fuel_cost = _get_fuel_cost(length, segment.vehicle_type)
    time_cost = _get_time_cost(segment.duration)
    depreciation_cost = _get_depreciation_cost(length, segment.vehicle_type)
    operation_cost = _get_operation_cost(length, segment.vehicle_type)
    return models.Cost.objects.create(
        segment=segment,
        fuel_cost=fuel_cost,
        time_cost=time_cost,
        depreciation_cost=depreciation_cost,
        operation_cost=operation_cost,
        total_cost=fuel_cost + time_cost + depreciation_cost + operation_cost
    )


def calculate_segment_health(segment, speed):
    return models.Health.objects.create(
        segment=segment,
        calories_consumed=_get_consumed_calories(
            speed, segment.duration, segment.vehicle_type),
        # benefit_index=None  # TODO
    )


def _calculate_emissions(segment_length, vehicle_type):
    return {
        "so2": _constants.SO2[vehicle_type] * segment_length,
        "nox": _constants.NOX[vehicle_type] * segment_length,
        "co2": _constants.CO2[vehicle_type] * segment_length,
        "co": _constants.CO[vehicle_type] * segment_length,
        "pm10": _constants.PM10[vehicle_type] * segment_length,
    }


def _get_fuel_cost(length, vehicle_type):
    try:
        volume_spent = length * _constants.FUEL_CONSUMPTION[vehicle_type]
        monetary_cost = volume_spent * _constants.FUEL_PRICE[vehicle_type]
    except KeyError:
        monetary_cost = 0
    return monetary_cost


def _get_time_cost(duration):
    duration_hours = duration.seconds / (60 * 60)
    return duration_hours * _constants.TIME_COST_PER_HOUR_EURO


def _get_depreciation_cost(length, vehicle_type):
    try:
        return length * _constants.DEPRECIATION_COST[vehicle_type]
    except KeyError:
        return 0


def _get_operation_cost(length, vehicle_type):
    try:
        return length * _constants.OPERATION_COST[vehicle_type]
    except KeyError:
        return 0


def _get_consumed_calories(speed, duration, vehicle_type):
    duration_minutes = duration.seconds / 60
    try:
        steps = _constants.CALORY_CONSUMPTION[vehicle_type]["steps"]
    except KeyError:
        result = 0
    else:
        for step in steps:
            if speed < step["speed"]:
                consumption_per_minute = step["calories"]
                break
        else:
            consumption_per_minute = steps[-1]["calories"]
        result = consumption_per_minute * duration_minutes
    return result
