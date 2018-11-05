#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib.admin import register
from django.contrib.gis.admin import OSMGeoAdmin

from . import models


@register(models.BikeObservation)
class BikeObservationAdmin(OSMGeoAdmin):
    pass