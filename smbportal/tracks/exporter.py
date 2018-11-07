#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from functools import partial
import logging
import pathlib

from osgeo import gdal
from osgeo import ogr

from . import models
from base.exporter import export_model_with_ogr
from base.exporter import FieldDef
from base.exporter import get_attribute_field
from base.exporter import get_related_model

logger = logging.getLogger(__name__)
gdal.UseExceptions()


def export_segments(segments, output_path: pathlib.Path,
                    driver_name="ESRI Shapefile"):
    """Export segments with OGR"""
    fields = [
        FieldDef(
            "track", ogr.OFTInteger,
            get_attribute_field, ("track_id",)
        ),
        FieldDef(
            "valid", ogr.OFTInteger,
            get_related_model, ("track", "is_valid", int)
        ),
        FieldDef(
            "vehicle", ogr.OFTString,
            get_attribute_field, ("vehicle_type",)
        ),
        FieldDef(
            "start", ogr.OFTString,
            get_attribute_field, ("start_date", str)),
        FieldDef(
            "end", ogr.OFTString,
            get_attribute_field, ("end_date", str)),
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
            get_related_model, ("emission", "so2",)),
        FieldDef(
            "nox_spent", ogr.OFTReal,
            get_related_model, ("emission", "nox",)),
        FieldDef(
            "co2_spent", ogr.OFTReal,
            get_related_model, ("emission", "co2",)),
        FieldDef(
            "co_spent", ogr.OFTReal,
            get_related_model, ("emission", "co",)),
        FieldDef(
            "pm10_spent", ogr.OFTReal,
            get_related_model, ("emission", "pm10",)
        ),
        FieldDef(
            "so2_saved", ogr.OFTReal,
            get_related_model, ("emission", "so2_saved",)
        ),
        FieldDef(
            "nox_saved", ogr.OFTReal,
            get_related_model, ("emission", "nox_saved",)
        ),
        FieldDef(
            "co2_saved", ogr.OFTReal,
            get_related_model, ("emission", "co2_saved",)
        ),
        FieldDef(
            "co_saved", ogr.OFTReal,
            get_related_model, ("emission", "co_saved",)
        ),
        FieldDef(
            "pm10_saved", ogr.OFTReal,
            get_related_model, ("emission", "pm10_saved",)
        ),
        FieldDef(
            "cost_fuel", ogr.OFTReal,
            get_related_model, ("cost", "fuel_cost",)
        ),
        FieldDef(
            "cost_time", ogr.OFTReal,
            get_related_model, ("cost", "time_cost",)
        ),
        FieldDef(
            "cost_depreciation"[:10], ogr.OFTReal,
            get_related_model, ("cost", "depreciation_cost",)
        ),
        FieldDef(
            "cost_operation"[:10], ogr.OFTReal,
            get_related_model, ("cost", "operation_cost",)
        ),
        FieldDef(
            "cost_total", ogr.OFTReal,
            get_related_model, ("cost", "total_cost",)
        ),
        FieldDef(
            "calories_consumed"[:10], ogr.OFTReal,
            get_related_model, ("health", "calories_consumed",)
        ),
        FieldDef(
            "benefit_index"[:10], ogr.OFTReal,
            get_related_model, ("health", "benefit_index",)
        ),
    ]
    return export_model_with_ogr(segments, output_path, fields, driver_name)


def get_minutes(segment: models.Segment):
    duration = segment.duration
    day_minutes = duration.days * 24 * 60
    second_minutes = duration.seconds / 60
    return day_minutes + second_minutes


def get_length(segment: models.Segment):
    return segment.get_length().km


def get_speed(segment: models.Segment):
    return segment.get_average_speed()


