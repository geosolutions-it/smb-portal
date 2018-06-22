#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django_filters import rest_framework as django_filters

import vehiclemonitor.models


class BikeObservationFilterset(django_filters.FilterSet):
    class Meta:
        model = vehiclemonitor.models.BikeObservation
        fields = [
            "bike",
        ]