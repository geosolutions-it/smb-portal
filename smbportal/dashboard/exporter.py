#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from collections import namedtuple
from functools import partial
import logging
import pathlib

from osgeo import gdal
from osgeo import ogr

import tracks.models
import prizes.models

gdal.UseExceptions()

logger = logging.getLogger(__name__)


FieldDef = namedtuple("FieldDef", [
    "name",
    "ogr_type",
    "value_getter",
    "value_getter_args",
])


def export_collected_points(collected_points, output_path: pathlib.Path,
                            driver_name="CSV"):
    geom_attribute_name = "the_geom"
    fields = [
        FieldDef(
            "id", ogr.OFTInteger,
            _get_attribute_field, ("id",),
        ),
        FieldDef(
            "vehicle_type", ogr.OFTString,
            _get_attribute_field, ("vehicle_type",),
        ),
        FieldDef(
            "track", ogr.OFTInteger,
            _get_attribute_field, ("track_id",),
        ),
        FieldDef(
            "longitude", ogr.OFTReal,
            get_coordinate, ("longitude", geom_attribute_name),
        ),
        FieldDef(
            "latitude", ogr.OFTReal,
            get_coordinate, ("latitude", geom_attribute_name),
        ),
        FieldDef(
            "sessionid", ogr.OFTString,
            _get_attribute_field, ("sessionid", str),
        ),
        FieldDef(
            "timestamp", ogr.OFTString,
            _get_attribute_field, ("timestamp", str),
        ),
        FieldDef(
            "acceleration_x", ogr.OFTReal,
            _get_attribute_field, ("accelerationx",),
        ),
        FieldDef(
            "acceleration_y", ogr.OFTReal,
            _get_attribute_field, ("accelerationy",),
        ),
        FieldDef(
            "acceleration_z", ogr.OFTReal,
            _get_attribute_field, ("accelerationz",),
        ),
        FieldDef(
            "accuracy", ogr.OFTReal,
            _get_attribute_field, ("accuracy",),
        ),
        FieldDef(
            "battery_consumption_per_hour", ogr.OFTReal,
            _get_attribute_field, ("batconsumptionperhour",),
        ),
        FieldDef(
            "battery_level", ogr.OFTReal,
            _get_attribute_field, ("batterylevel",),
        ),
        FieldDef(
            "device_bearing", ogr.OFTReal,
            _get_attribute_field, ("devicebearing",),
        ),
        FieldDef(
            "device_pitch", ogr.OFTReal,
            _get_attribute_field, ("devicepitch",),
        ),
        FieldDef(
            "device_roll", ogr.OFTReal,
            _get_attribute_field, ("deviceroll",),
        ),
        FieldDef(
            "elevation", ogr.OFTReal,
            _get_attribute_field, ("elevation",),
        ),
        FieldDef(
            "gps_bearing", ogr.OFTReal,
            _get_attribute_field, ("gps_bearing",),
        ),
        FieldDef(
            "humidity", ogr.OFTReal,
            _get_attribute_field, ("humidity",),
        ),
        FieldDef(
            "lumen", ogr.OFTReal,
            _get_attribute_field, ("lumen",),
        ),
        FieldDef(
            "proximity", ogr.OFTReal,
            _get_attribute_field, ("proximity",),
        ),
        FieldDef(
            "speed", ogr.OFTReal,
            _get_attribute_field, ("speed",),
        ),
        FieldDef(
            "temperature", ogr.OFTReal,
            _get_attribute_field, ("temperature",),
        ),

    ]
    return _export_model_with_ogr(
        collected_points, output_path, fields, driver_name,
        geom_attribute_name=geom_attribute_name
    )


def export_segments(segments, output_path: pathlib.Path,
                    driver_name="ESRI Shapefile"):
    """Export segments with OGR"""
    fields = [
        FieldDef(
            "track", ogr.OFTInteger,
            _get_attribute_field, ("track_id",)
        ),
        FieldDef("first_name", ogr.OFTString,
                 get_segment_owner_info, ("first_name",)),
        FieldDef("last_name", ogr.OFTString,
                 get_segment_owner_info, ("last_name",)),
        FieldDef("email", ogr.OFTString,
                 get_segment_owner_info, ("email",)),
        FieldDef(
            "valid", ogr.OFTInteger,
            _get_related_model, ("track", "is_valid", int)
        ),
        FieldDef(
            "vehicle", ogr.OFTString,
            _get_attribute_field, ("vehicle_type",)
        ),
        FieldDef(
            "start", ogr.OFTString,
            _get_attribute_field, ("start_date", str)),
        FieldDef(
            "end", ogr.OFTString,
            _get_attribute_field, ("end_date", str)),
        FieldDef(
            "minutes", ogr.OFTReal,
            get_minutes, None),
        FieldDef(
            "length_km", ogr.OFTReal,
            get_length, None),
        FieldDef(
            "speed_km_h", ogr.OFTReal,
            get_speed, None),
        FieldDef(
            "so2_spent", ogr.OFTReal,
            _get_related_model, ("emission", "so2",)),
        FieldDef(
            "nox_spent", ogr.OFTReal,
            _get_related_model, ("emission", "nox",)),
        FieldDef(
            "co2_spent", ogr.OFTReal,
            _get_related_model, ("emission", "co2",)),
        FieldDef(
            "co_spent", ogr.OFTReal,
            _get_related_model, ("emission", "co",)),
        FieldDef(
            "pm10_spent", ogr.OFTReal,
            _get_related_model, ("emission", "pm10",)
        ),
        FieldDef(
            "so2_saved", ogr.OFTReal,
            _get_related_model, ("emission", "so2_saved",)
        ),
        FieldDef(
            "nox_saved", ogr.OFTReal,
            _get_related_model, ("emission", "nox_saved",)
        ),
        FieldDef(
            "co2_saved", ogr.OFTReal,
            _get_related_model, ("emission", "co2_saved",)
        ),
        FieldDef(
            "co_saved", ogr.OFTReal,
            _get_related_model, ("emission", "co_saved",)
        ),
        FieldDef(
            "pm10_saved", ogr.OFTReal,
            _get_related_model, ("emission", "pm10_saved",)
        ),
        FieldDef(
            "cost_fuel", ogr.OFTReal,
            _get_related_model, ("cost", "fuel_cost",)
        ),
        FieldDef(
            "cost_time", ogr.OFTReal,
            _get_related_model, ("cost", "time_cost",)
        ),
        FieldDef(
            "cost_depreciation"[:10], ogr.OFTReal,
            _get_related_model, ("cost", "depreciation_cost",)
        ),
        FieldDef(
            "cost_operation"[:10], ogr.OFTReal,
            _get_related_model, ("cost", "operation_cost",)
        ),
        FieldDef(
            "cost_total", ogr.OFTReal,
            _get_related_model, ("cost", "total_cost",)
        ),
        FieldDef(
            "calories_consumed"[:10], ogr.OFTReal,
            _get_related_model, ("health", "calories_consumed",)
        ),
        FieldDef(
            "benefit_index"[:10], ogr.OFTReal,
            _get_related_model, ("health", "benefit_index",)
        ),
    ]
    return _export_model_with_ogr(segments, output_path, fields, driver_name)


def export_observations(observations, output_path: pathlib.Path,
                        driver_name="CSV"):
    geom_attribute_name = "position"
    fields = [
        FieldDef(
            "bike", ogr.OFTString,
            _get_related_model, ("bike", "short_uuid"),
        ),
        FieldDef(
            "longitude", ogr.OFTReal,
            get_coordinate, ("longitude", geom_attribute_name),
        ),
        FieldDef(
            "latitude", ogr.OFTReal,
            get_coordinate, ("latitude", geom_attribute_name),
        ),
        FieldDef(
            "address", ogr.OFTString,
            _get_attribute_field, ("address",),
        ),
        FieldDef(
            "observed", ogr.OFTString,
            _get_attribute_field, ("observed_at", str),
        ),
        FieldDef(
            "reporter_id", ogr.OFTString,
            _get_attribute_field, ("reporter_id", str),
        ),
        FieldDef(
            "reporter_type", ogr.OFTString,
            _get_attribute_field, ("reporter_type", str),
        ),
        FieldDef(
            "details", ogr.OFTString,
            _get_attribute_field, ("details",),
        ),
    ]
    return _export_model_with_ogr(
        observations, output_path, fields, driver_name,
        geom_attribute_name=geom_attribute_name
    )


def export_bike_statuses(statuses, output_path: pathlib.Path,
                         driver_name="CSV"):
    geom_attribute_name = "position"
    fields = [
        FieldDef(
            "bike", ogr.OFTString,
            _get_related_model, ("bike", "short_uuid"),
        ),
        FieldDef(
            "lost", ogr.OFTInteger,
            _get_attribute_field, ("lost", int)
        ),
        FieldDef(
            "creation_date", ogr.OFTString,
            _get_attribute_field, ("creation_date", str),
        ),
        FieldDef(
            "details", ogr.OFTString,
            _get_attribute_field, ("details",),
        ),
        FieldDef(
            "longitude", ogr.OFTReal,
            get_coordinate, ("longitude", geom_attribute_name),
        ),
        FieldDef(
            "latitude", ogr.OFTReal,
            get_coordinate, ("latitude", geom_attribute_name),
        ),
    ]
    return _export_model_with_ogr(
        statuses, output_path, fields, driver_name,
        geom_attribute_name=geom_attribute_name
    )


def export_competition_winners(winners, output_path: pathlib.Path):
    fields = [
        FieldDef(
            "username", ogr.OFTString,
            _get_related_model, ("user", "username"),
        ),
        FieldDef(
            "first_name", ogr.OFTString,
            _get_related_model, ("user", "first_name"),
        ),
        FieldDef(
            "last_name", ogr.OFTString,
            _get_related_model, ("user", "last_name"),
        ),
        FieldDef(
            "email", ogr.OFTString,
            _get_related_model, ("user", "email"),
        ),
        FieldDef(
            "phone_number", ogr.OFTString,
            get_profile_info, ("phone_number",),
        ),
        FieldDef(
            "age", ogr.OFTString,
            get_profile_info, ("age",),
        ),
        FieldDef(
            "competition_name", ogr.OFTString,
            _get_related_model, ("competition", "name")
        ),
        FieldDef(
            "competition_start", ogr.OFTString,
            _get_related_model, ("competition", "start_date", str),
        ),
        FieldDef(
            "competition_end", ogr.OFTString,
            _get_related_model, ("competition", "end_date", str),
        ),
        FieldDef(
            "competition_age_groups", ogr.OFTString,
            get_competition_age_groups, None,
        ),
        FieldDef(
            "rank", ogr.OFTInteger,
            _get_attribute_field, ("rank", int),
        ),
        FieldDef(
            "prize_name", ogr.OFTString,
            get_prize_info, ("prize_names",),
        ),
        FieldDef(
            "prize_sponsor", ogr.OFTString,
            get_prize_info, ("sponsor_names",),
        ),
    ]
    return _export_model_with_ogr(winners, output_path, fields, "CSV")


def get_coordinate(model_obj, coordinate: str, geometry_attribute_name):
    attribute = {
        "latitude": "y",
        "longitude": "x",
    }.get(coordinate)
    geom = getattr(model_obj, geometry_attribute_name)
    return getattr(geom, attribute) if geom is not None else None


def get_minutes(segment: tracks.models.Segment):
    duration = segment.duration
    day_minutes = duration.days * 24 * 60
    second_minutes = duration.seconds / 60
    return day_minutes + second_minutes


def get_segment_owner_info(segment: tracks.models.Segment, attribute,
                           cast_to=None):
    value = getattr(segment.track.owner, attribute, "")
    return cast_to(value) if cast_to is not None else value


def get_length(segment: tracks.models.Segment):
    return segment.get_length().km


def get_speed(segment: tracks.models.Segment):
    return segment.get_average_speed()


def get_prize_info(winner: prizes.models.Winner, info: str):
    competition_prizes = winner.competition.competitionprize_set.filter(
        user_rank=winner.rank)
    if info == "prize_names":
        result = ";".join(cp.prize.name for cp in competition_prizes)
    elif info == "sponsor_names":
        result = ";".join(cp.prize.sponsor.name for cp in competition_prizes)
    else:
        result = ""
    return result


def get_profile_info(winner: prizes.models.Winner, info: str):
    return getattr(winner.user.profile, info, "")


def get_competition_age_groups(winner: prizes.models.Winner):
    return "; ".join(g for g in winner.competition.age_groups)


def _export_model_with_ogr(objects, output_path: pathlib.Path,
                           field_definitions, driver_name="ESRI Shapefile",
                           geom_attribute_name="geom"):
    driver = ogr.GetDriverByName(driver_name)
    data_source = driver.CreateDataSource(str(output_path))
    layer = data_source.CreateLayer(
        "track_segments", geom_type=ogr.wkbLineString)
    for field_def in field_definitions:
        output_field = ogr.FieldDefn(field_def.name, field_def.ogr_type)
        layer.CreateField(output_field)
    for obj in objects:
        feature_def = layer.GetLayerDefn()
        feature = ogr.Feature(feature_def)
        django_geom = getattr(obj, geom_attribute_name, None)
        if django_geom is not None:
            ogr_geom = ogr.CreateGeometryFromWkb(bytes(django_geom.wkb))
            feature.SetGeometry(ogr_geom)
        for field in field_definitions:
            field_value = _get_field_value(obj, field)
            feature.SetField(field.name, field_value)
        layer.CreateFeature(feature)
        feature = None
    data_source = None


def _get_field_value(obj, field_def):
    handler = partial(field_def.value_getter, obj)
    args = field_def.value_getter_args
    return handler(*args) if args is not None else handler()


def _get_attribute_field(obj, attribute_name: str, cast_to=None):
    value = getattr(obj, attribute_name)
    cast_value = cast_to(value) if cast_to is not None else value
    return cast_value


def _get_related_model(obj, related_attribute: str, model_attribute: str,
                       cast_to=None, default_value=0):
    related_obj = getattr(obj, related_attribute, None)
    value = getattr(related_obj, model_attribute, None)
    value = value if value is not None else default_value
    return cast_to(value) if cast_to is not None else value
