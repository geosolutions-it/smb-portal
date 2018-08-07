#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiLineString
from django.core.management.base import BaseCommand
from django.db import connection

from tracks import models


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
                # self.stdout.write("-- Simulating emissions cost and health...")
                # for segment in segments:
                #     emissions = simulate_segment_emissions(segment)
                #     costs = simulate_segment_cost(segment)
                #     health = simulate_segment_health(segment)


def create_segments(track, vehicle_type, points_per_segment=50):
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
                the_geom=MultiLineString(linestring),
                start_date=start,
                end_date=end,
            )
            segments.append(segment)
    return segments


def simulate_segment_emissions(segment):
    pass


def simulate_segment_cost(segment):
    pass

def simulate_segment_health(segment):
    pass
