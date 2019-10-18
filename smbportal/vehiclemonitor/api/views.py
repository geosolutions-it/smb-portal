#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework_gis.pagination import GeoJsonPagination

from .. import models
from . import filters
from . import serializers

logger = logging.getLogger(__name__)

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class MyBikeObservationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.MyBikeObservationSerializer
    required_permissions = (
        "vehiclemonitor.can_list_own_bike_observation",
    )
    pagination_class = GeoJsonPagination
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BikeObservationFilterSet

    def get_queryset(self):
        return models.BikeObservation.objects.filter(
            bike__owner=self.request.user)


class BikeObservationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = serializers.BikeObservationSerializer
    required_permissions = (
        "vehiclemonitor.can_list_bike_observation",
    )
    queryset = models.BikeObservation.objects.all()
