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
import logging
import pathlib
from typing import List

from osgeo import gdal
from osgeo import ogr

from base.exporter import export_model_with_ogr
from base.exporter import FieldDef
from base.exporter import get_attribute_field
from base.exporter import get_related_model

from . import models

gdal.UseExceptions()

logger = logging.getLogger(__name__)



def export_observations(observations, output_path: pathlib.Path,
                        driver_name="CSV"):
    fields = [
        FieldDef(
            "bike", ogr.OFTString,
            get_related_model, ("bike", "short_uuid"),
        ),
        FieldDef(
            "longitude", ogr.OFTReal,
            get_coordinate, ("longitude",),
        ),
        FieldDef(
            "latitude", ogr.OFTReal,
            get_coordinate, ("latitude",),
        ),
        FieldDef(
            "address", ogr.OFTString,
            get_attribute_field, ("address",),
        ),
        FieldDef(
            "observed", ogr.OFTString,
            get_attribute_field, ("observed_at", str),
        ),
        FieldDef(
            "reporter_id", ogr.OFTString,
            get_attribute_field, ("reporter_id", str),
        ),
        FieldDef(
            "reporter_type", ogr.OFTString,
            get_attribute_field, ("reporter_type", str),
        ),
        FieldDef(
            "details", ogr.OFTString,
            get_attribute_field, ("details",),
        ),
    ]
    return export_model_with_ogr(
        observations, output_path, fields, driver_name,
        geom_attribute_name="position"
    )


def get_coordinate(observation: models.BikeObservation, coordinate: str):
    attribute = {
        "latitude": "y",
        "longitude": "x",
    }.get(coordinate)
    position = observation.position
    return getattr(position, attribute) if position is not None else None

