#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as gismodels


class Track(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class CollectedPoint(gismodels.Model):
    BIKE = "bike"
    BUS = "bus"

    vehicle_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Identifier of the vehicle used, if any"
    )
    vehicle_type = models.CharField(
        max_length=50,
        choices=(
            (BIKE, BIKE),
            (BUS, BUS),
        ),
        default=BIKE,
        null=True,
        blank=True
    )
    track = models.ForeignKey(
        "Track",
        on_delete=models.CASCADE
    )
    the_geom = gismodels.PointField()
    accelerationx = models.FloatField(blank=True, null=True)
    accelerationy = models.FloatField(blank=True, null=True)
    accelerationz = models.FloatField(blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    batconsumptionperhour = models.FloatField(blank=True, null=True)
    batterylevel = models.FloatField(blank=True, null=True)
    devicebearing = models.FloatField(blank=True, null=True)
    devicepitch = models.FloatField(blank=True, null=True)
    deviceroll = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    gps_bearing = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    lumen = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    proximity = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    icon_color = models.BigIntegerField(blank=True, null=True)
    sessionid = models.BigIntegerField(blank=True, null=True)
