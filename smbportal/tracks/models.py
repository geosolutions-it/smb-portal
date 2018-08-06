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
from django.utils.translation import gettext_lazy as _

BIKE = "bike"
BUS = "bus"
CAR = "car"
FOOT = "foot"


class Track(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


class CollectedPoint(gismodels.Model):

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
    temperature = models.FloatField(blank=True, null=True)
    icon_color = models.BigIntegerField(blank=True, null=True)
    sessionid = models.BigIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)


class Segment(gismodels.Model):
    """Stores a computed segment from a track.

    Computation is made from the relevant :model:`tracks.CollectedPoint`
    instances.

    """

    track = models.ForeignKey(
        "Track",
        on_delete=models.CASCADE,
        verbose_name=_("track")
    )
    user_uuid = models.ForeignKey(
        "bossoidc.Keycloak",
        on_delete=models.CASCADE,
        db_column="user_uuid",
        verbose_name=_("user uuid"),
    )
    vehicle_type = models.CharField(
        _("vehicle type"),
        max_length=20,
        choices=(
            (BIKE, _("bike")),
            (BUS, _("bus")),
            (CAR, _("car")),
            (FOOT, _("foot")),
        )
    )
    the_geom = gismodels.MultiLineStringField(
        _("geometry")
    )
    start_date = models.DateTimeField(
        _("start date"),
        help_text=_("timestamp of first collected point of the segment"),
    )
    end_date = models.DateTimeField(
        _("end date"),
        help_text=_("timestamp of last collected point of the segment")
    )

    def __str__(self):
        return "{0.track} - {0.vehicle_type} - {0.start_date}".format(self)


class Emission(models.Model):
    segment = models.ForeignKey(
        "Segment",
        on_delete=models.CASCADE,
        verbose_name=_("segment")
    )
    so2 = models.FloatField(
        _("SO2"),
        null=True,
        blank=True,
        help_text=_("Sulphur Dioxide emissions (mg)")
    )
    so2_saved = models.FloatField(
        _("SO2 saved"),
        null=True,
        blank=True,
        help_text=_("Dulphur Dioxide emissions that were prevented (mg)")
    )
    nox = models.FloatField(
        _("NOx"),
        null=True,
        blank=True,
        help_text=_("Nitrogen Oxides emissions (mg)")
    )
    nox_saved = models.FloatField(
        _("NOx saved"),
        null=True,
        blank=True,
        help_text=_("Nitrogen Oxides emissions that were prevented (mg)")
    )
    co2 = models.FloatField(
        _("CO2"),
        null=True,
        blank=True,
        help_text=_("Carbon dioxide emissions (g)")
    )
    co2_saved = models.FloatField(
        _("CO2 saved"),
        null=True,
        blank=True,
        help_text=_("Carbon dioxide emissions that were prevented (g)")
    )
    co = models.FloatField(
        _("CO"),
        null=True,
        blank=True,
        help_text=_("Carbon monoxide emissions (mg)")
    )
    co_saved = models.FloatField(
        _("CO saved"),
        null=True,
        blank=True,
        help_text=_("Carbon monoxide emissions that were prevented (mg)")
    )
    pm10 = models.FloatField(
        _("PM10"),
        null=True,
        blank=True,
        help_text=_("Particulate Matter up to 10um emissions (mg)")
    )
    pm10_saved = models.FloatField(
        _("PM10 saved"),
        null=True,
        blank=True,
        help_text=_("Particulate Matter up to 10um emissions that "
                    "were prevented (mg)")
    )


class Cost(models.Model):
    segment = models.ForeignKey(
        "Segment",
        on_delete=models.CASCADE,
        verbose_name=_("segment")
    )
    fuel_cost = models.FloatField(
        _("fuel cost"),
        null=True,
        blank=True,
        help_text=_("Fuel consumption cost (eur)")
    )
    time_cost = models.FloatField(
        _("time cost"),
        null=True,
        blank=True,
        help_text=_("Time spent cost (eur)")
    )
    depreciation_cost = models.FloatField(
        _("depreciation cost"),
        null=True,
        blank=True,
        help_text=_("Vehicle depreciation cost (eur)")
    )
    operation_cost = models.FloatField(
        _("operational cost"),
        null=True,
        blank=True,
        help_text=_("Vehicle operation cost (eur)")
    )
    total_cost = models.FloatField(
        _("total cost"),
        null=True,
        blank=True,
        help_text=_("Total cost (eur)")
    )

    def __str__(self):
        return "{0.segment} - {0.total_cost}".format(self)


class Health(models.Model):
    segment = models.ForeignKey(
        "Segment",
        on_delete=models.CASCADE,
        verbose_name=_("segment")
    )
    calories_consumed = models.FloatField(
        _("calories consumed"),
        null=True,
        blank=True,
        help_text=_("Calories consumed (cal)")
    )
    benefit_index = models.FloatField(
        _("benefit index"),
        null=True,
        blank=True,
        help_text=_("Benefit Index, adapted from World Health Organization's "
                    "'Health economic assessment tools (HEAT) for walking "
                    "and for cycling - Methods and user guide on physical "
                    "activity, air pollution, injuries and carbon impact "
                    "assessments'")
    )

    def __str__(self):
        return "{0.segment} - {0.benefit_index}".format(self)
