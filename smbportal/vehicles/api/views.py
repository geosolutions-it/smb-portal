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

from rest_framework import mixins
from rest_framework import viewsets


from .. import models
from . import filters
from . import serializers


logger = logging.getLogger(__name__)


class MyBikeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyBikeDetailSerializer
    required_permissions = (
        "vehicles.can_list_own_bikes",
        "vehicles.can_create_bike",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"

    def get_queryset(self):
        return models.Bike.objects.filter(owner=self.request.user)


class MyPhysicalTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.MyPhysicalTagSerializer
    required_permissions = (
        "vehicles.can_list_own_physical_tags",
    )
    lookup_field = "epc"

    def get_queryset(self):
        return models.PhysicalTag.objects.filter(
            bike__owner=self.request.user)


class MyBikeStatusViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.MyBikeStatusSerializer
    required_permissions = (
        "vehicles.can_list_own_bike_status",
        "vehicles.can_create_own_bike_status",
    )

    def get_queryset(self):
        return models.BikeStatus.objects.filter(
            bike__owner=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = kwargs.pop("context", {})
        context.update({
            "request": self.request
        })
        return serializer_class(context=context, *args, **kwargs)


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikeDetailSerializer
    queryset = models.Bike.objects.all()
    required_permissions = (
        "vehicles.can_list_bikes",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"


class PhysicalTagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,  mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    queryset = models.PhysicalTag.objects.all()
    required_permissions = (
        "vehicles.can_list_physical_tags",
        "vehicles.can_create_physical_tag",
    )
    lookup_field = "epc"


class BikeStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikeStatusSerializer
    required_permissions = (
        "vehicles.can_list_bike_status",
    )

    def get_queryset(self):
        return models.BikeStatus.objects.all()
