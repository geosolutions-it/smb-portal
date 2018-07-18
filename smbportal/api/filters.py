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

import profiles.models
import vehicles.models
import vehiclemonitor.models


class BikeFilterSet(django_filters.FilterSet):
    short_uuid = django_filters.CharFilter(
        lookup_expr="istartswith",
    )
    tag = django_filters.CharFilter(
        name="tags__epc",
        lookup_expr="istartswith"
    )

    class Meta:
        model = vehicles.models.Bike
        fields = [
            "short_uuid",
            "tag",
        ]


class BikeObservationFilterSet(django_filters.FilterSet):
    bike = django_filters.CharFilter(
        field_name="bike__short_uuid",
        lookup_expr="istartswith",
    )

    class Meta:
        model = vehiclemonitor.models.BikeObservation
        fields = [
            "bike",
        ]


class SmbUserFilterSet(django_filters.FilterSet):
    class Meta:
        model = profiles.models.SmbUser
        fields = [
            "username"
        ]
