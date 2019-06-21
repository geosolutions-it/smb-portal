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


class BikeFilterSet(django_filters.FilterSet):
    short_uuid = django_filters.CharFilter(
        lookup_expr="istartswith",
    )
    tag = django_filters.CharFilter(
        name="tags__epc",
        lookup_expr="istartswith"
    )

    class Meta:
        model = models.Bike
        fields = [
            "short_uuid",
            "tag",
        ]


