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
import hashlib
import pathlib

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from lxml import etree
import pytz

from vehicles.models import Bike
from tracks import models


class Command(BaseCommand):
    help = ("Add test data for tracks")

    def add_arguments(self, parser):
        parser.add_argument(
            "gpx-file-path",
            help="Path to a gpx file with tracks to add"
        )
        parser.add_argument(
            "point-owner-info",
            nargs="+",
            help="Users and vehicles that will own the created tracks and "
                 "points. This argument takes the form "
                 "`username:bike_nickname`. The existing GPX tracks will be "
                 "split out evenly between the user/bike pairs. Each track "
                 "will also assign 90%% of its points to the selected bike, "
                 "the remaining points will be assigned to a BUS vehicle "
                 "type. Example: 'manage.py populatetracks tracks.gpx user1:bike1 user1:bike2 user2:bike3 "
                 "user4:bike4'. The preceding example means that the tracks "
                 "present in the `tracks.gpx` file will be imported. User1 "
                 "will be the owner of 50%% of the existing tracks, user2 will "
                 "own 25%% and user3 will own the remaining 25%%."
        )

    def handle(self, *args, **options):
        gpx_path = pathlib.Path(options["gpx-file-path"])
        owner_info = [item.split(":") for item in options["point-owner-info"]]
        self.stdout.write("Parsing gpx file...")
        all_tracks = get_tracks_from_gpx(gpx_path)
        self.stdout.write("Creating tracks and points...")
        save_tracks(all_tracks, owner_info)
        self.stdout.write("Done!")


@transaction.atomic
def save_tracks(imported_tracks,owner_info):
    for track_index, imported_track in enumerate(imported_tracks):
        owner_index = _map_track_to_user(
            len(owner_info), len(imported_tracks), track_index)
        username, bike_nickname = owner_info[owner_index]
        user = get_user_model().objects.get(username=username)
        bike = Bike.objects.get(owner=user, nickname=bike_nickname)
        save_track(user, bike, imported_track)


def save_track(user, bike, track_points):
    track = models.Track.objects.create(owner=user)
    for pt_index, point in enumerate(track_points):
        if pt_index < len(track_points) * 0.9:
            vehicle_id = bike.id
            vehicle_type = models.CollectedPoint.BIKE
        else:
            vehicle_id = None
            vehicle_type = models.CollectedPoint.BUS
        models.CollectedPoint.objects.create(
            vehicle_id=vehicle_id,
            vehicle_type=vehicle_type,
            track=track,
            the_geom=Point(point["lon"], point["lat"]),
            timestamp=point.get("timestamp"),
        )
    return track


def get_tracks_from_gpx(gpx_path: pathlib.Path):
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
            except IndexError:
                pass
            else:
                collected_point["timestamp"] = point_date
            segment.append(collected_point)
        tracks.append(segment)
    return tracks


def _get_time(raw_time: str):
    return pytz.utc.localize(
        dt.datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%SZ")
    )


def _map_track_to_user(num_users, num_tracks, current_track):
    return int(current_track / num_tracks * num_users)

