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
import pathlib
from typing import Dict
from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree
import pytz

from keycloakauth.keycloakadmin import get_manager
from keycloakauth.utils import create_user
from keycloakauth.utils import delete_user
from vehicles.models import Bike
import profiles.models as pm
from tracks import models

from . import _constants


ImportedTrack = List[Dict]


class Command(BaseCommand):
    help = (
        "Add test data for tracks and segments. This command adds users, "
        "bikes, tracks, segments and collected points to the database. The "
        "users are created also on keycloak. Usernames of the new users: "
        "`track_tester1`, `track_tester2` and `track_tester3`"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keycloak_manager = get_manager(
            settings.KEYCLOAK["base_url"],
            settings.KEYCLOAK["realm"],
            settings.KEYCLOAK["client_id"],
            settings.KEYCLOAK["admin_username"],
            settings.KEYCLOAK["admin_password"],
        )

    def add_arguments(self, parser):
        default_gpx_path = pathlib.Path(
            settings.BASE_DIR).parent / "tests" / "data" / "tracks.gpx"
        parser.add_argument(
            "--recreate-data",
            action="store_true",
            help="Whether to drop existing test users (and all data owned by "
                 "them)",
        )
        parser.add_argument(
            "--gpx-file-path",
            help="Path to a gpx file with tracks to add. Defaults to "
                 "%(default)r",
            default=str(default_gpx_path)
        )

    def handle(self, *args, **options):
        gpx_path = pathlib.Path(
            options["gpx_file_path"],
        )
        owners = {
            "track_tester1": {
                "age": pm.EndUserProfile.AGE_BETWEEN_NINETEEN_AND_THIRTY,
                "occupation": pm.EndUserProfile.OCCUPATION_ARCHITECT,
            },
            "track_tester2": {
                "age": pm.EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
                "occupation": pm.EndUserProfile.OCCUPATION_FREELANCER,
            },
            "track_tester3": {
                "age": pm.EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
                "occupation": pm.EndUserProfile.OCCUPATION_UNEMPLOYED,
            },
        }
        try:
            users = create_test_users(owners, self.keycloak_manager,
                                      options["recreate_data"])
        except RuntimeError as exc:
            self.stderr.write("{} - Aborting".format(str(exc)))
        else:
            self.stdout.write("Parsing gpx file...")
            all_tracks = get_tracks_from_gpx(gpx_path)
            save_tracks(all_tracks, users, logger=self.stdout.write)
        self.stdout.write("Done!")


def create_test_users(users_info, keycloak_manager, recreate_users):
    if users_exist(users_info.keys()):
        if recreate_users:
            for username in users_info.keys():
                delete_user(username, keycloak_manager)
        else:
            raise RuntimeError("Users already exist")
    users = []
    for index, user_info in enumerate(users_info.items()):
        username, profile_kwargs = user_info
        user = create_user(
            username,
            email="{}@fake.com".format(username),
            password="123456",
            group_path="/end_users",
            keycloak_manager=keycloak_manager,
            profile_model=pm.EndUserProfile,
            profile_kwargs=profile_kwargs
        )
        for bike_index in range(2):
            nickname = "bike_{}_{}".format(index, bike_index)
            Bike.objects.create(nickname=nickname, owner=user)
        users.append(user)
    return users


def users_exist(usernames: list) -> bool:
    return pm.SmbUser.objects.filter(
        username__in=usernames).count() != 0


@transaction.atomic
def save_tracks(imported_tracks: List[ImportedTrack], users, logger=print):
    owner_info = _unfold_users(users)
    for track_index, imported_track in enumerate(imported_tracks):
        logger("Processing track {}/{}...".format(
            track_index+1, len(imported_tracks)))
        owner_index = _map_track_to_user(
            len(owner_info), len(imported_tracks), track_index)
        username, bike_nickname = owner_info[owner_index]
        user = get_user_model().objects.get(username=username)
        bike = Bike.objects.get(owner=user, nickname=bike_nickname)
        save_track(user, bike, imported_track)


def save_track(user, bike, track_points: ImportedTrack):
    track = models.Track.objects.create(owner=user)
    for pt_index, point in enumerate(track_points):
        if pt_index < len(track_points) * 0.9:
            vehicle_id = bike.id
            vehicle_type = models.BIKE
        else:
            vehicle_id = None
            vehicle_type = models.BUS
        models.CollectedPoint.objects.create(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            track=track,
            the_geom=Point(point["lon"], point["lat"]),
            timestamp=point.get("timestamp"),
        )
    bike_segments = create_segments(track, models.BIKE)
    bus_segments = create_segments(track, models.BUS)
    for segment in bike_segments + bus_segments:
        length = segment.get_length().km
        speed = segment.get_average_speed()
        calculate_segment_emissions(segment, length)
        calculate_segment_cost(segment, length)
        calculate_segment_health(segment, speed)
    return track


def get_tracks_from_gpx(gpx_path: pathlib.Path) -> List[ImportedTrack]:
    """Generate collected points from a gpx file

    We transform each of the GPX's track segment into a track

    """

    gpx = etree.fromstring(
        gpx_path.read_bytes(),
        parser=etree.XMLParser(resolve_entities=False)
    )
    nsmap = {
        "gpx": gpx.nsmap[None]
    }
    track_segments = gpx.xpath("gpx:trk/gpx:trkseg", namespaces=nsmap)
    tracks = []
    for segment_element in track_segments:
        segment = []
        for point in segment_element.xpath("gpx:trkpt", namespaces=nsmap):
            collected_point = {
                "lat": float(point.get("lat")),
                "lon": float(point.get("lon")),
            }
            try:
                point_date = _get_time(
                    point.xpath("gpx:time/text()", namespaces=nsmap)[0]
                )
            except IndexError:  # discard points that don't have a timestamp
                pass
            else:
                collected_point["timestamp"] = point_date
                segment.append(collected_point)
        if len(segment) > 1:  # discard segments with only one point
            tracks.append(segment)
    return tracks


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
            start = min([pt.timestamp for pt in pts])
            end = max([pt.timestamp for pt in pts])
            segment, created = models.Segment.objects.get_or_create(
                track=track,
                user_uuid=track.owner.keycloak,
                vehicle_type=vehicle_type,
                vehicle_id=pts[-1].vehicle_id,
                geom=LineString([pt.the_geom.coords for pt in pts]),
                start_date=start,
                end_date=end,
            )
            segments.append(segment)
    return segments


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


def _unfold_users(users):
    owner_info = []
    for user in users:
        for bike in user.bikes.all():
            owner_info.append((user, bike))
    return owner_info


def _get_time(raw_time: str):
    return pytz.utc.localize(
        dt.datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
    )


def _map_track_to_user(num_users, num_tracks, current_track):
    return int(current_track / num_tracks * num_users)


