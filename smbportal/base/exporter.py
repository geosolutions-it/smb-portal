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

gdal.UseExceptions()

logger = logging.getLogger(__name__)


FieldDef = namedtuple("FieldDef", [
    "name",
    "ogr_type",
    "value_getter",
    "value_getter_args",
])


def export_model_with_ogr(objects, output_path: pathlib.Path,
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
        django_geom = getattr(obj, geom_attribute_name)
        ogr_geom = ogr.CreateGeometryFromWkb(bytes(django_geom.wkb))
        feature.SetGeometry(ogr_geom)
        for field in field_definitions:
            field_value = get_field_value(obj, field)
            feature.SetField(field.name, field_value)
        layer.CreateFeature(feature)
        feature = None
    data_source = None


def get_field_value(obj, field_def):
    handler = partial(field_def.value_getter, obj)
    args = field_def.value_getter_args
    return handler(*args) if args is not None else handler()


def get_attribute_field(obj, attribute_name: str, cast_to=None):
    value = getattr(obj, attribute_name)
    return cast_to(value) if cast_to is not None else value


def get_related_model(obj, segment_attribute: str, model_attribute: str,
                      cast_to=None, default_value=0):
    related_obj = getattr(obj, segment_attribute, None)
    value = getattr(related_obj, model_attribute, None)
    value = value if value is not None else default_value
    return cast_to(value) if cast_to is not None else value


