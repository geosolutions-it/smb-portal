#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django_filters import rest_framework as django_filters

from .. import models


class BikeObservationFilterSet(django_filters.FilterSet):
    bike = django_filters.CharFilter(
        field_name="bike__short_uuid",
        lookup_expr="istartswith",
    )

    class Meta:
        model = models.BikeObservation
        fields = [
            "bike",
        ]
