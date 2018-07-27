#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging

from django_filters.rest_framework import DjangoFilterBackend
import photologue.models
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_gis.pagination import GeoJsonPagination

import profiles.models
import vehicles.models
import vehiclemonitor.models
from . import serializers
from . import filters

logger = logging.getLogger(__name__)

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class MyUserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.SmbUserSerializer
    required_permissions = (
        "profiles.can_view_profile",
    )
    required_object_permissions = (
        "profiles.can_edit_profile",
    )

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, obj=user.profile)
        return user


class MyBikeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BikeDetailSerializer
    required_permissions = (
        "vehicles.can_list_own_bikes",
        "vehicles.can_create_bike",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"

    def get_queryset(self):
        return vehicles.models.Bike.objects.filter(owner=self.request.user)


class MyBikeObservationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.BikeObservationSerializer
    required_permissions = (
        "vehiclemonitor.can_list_own_bike_observation",
    )
    pagination_class = GeoJsonPagination
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.BikeObservationFilterSet

    def get_queryset(self):
        return vehiclemonitor.models.BikeObservation.objects.filter(
            bike__owner=self.request.user)


class MyPhysicalTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    required_permissions = (
        "vehicles.can_list_own_physical_tags",
    )

    def get_queryset(self):
        return vehicles.models.PhysicalTag.objects.filter(
            bike__owner=self.request.user)


class MyBikeStatusViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.BikeStatusSerializer
    required_permissions = (
        "vehicles.can_list_own_bike_status",
        "vehicles.can_create_own_bike_status",
    )

    def get_queryset(self):
        return vehicles.models.BikeStatus.objects.filter(
            bike__owner=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = kwargs.pop("context", {})
        context.update({
            "request": self.request
        })
        return serializer_class(context=context, *args, **kwargs)


class SmbUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SmbUserSerializer
    queryset = profiles.models.SmbUser.objects.all()
    required_permissions = (
        "profiles.can_list_users",
    )
    lookup_field = "uuid"

    def get_object(self):
        obj = self.get_queryset().get(keycloak__UID=self.kwargs["uuid"])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True)
    def single_dump(self, request, uuid=None):
        user = self.get_object()
        serializer = serializers.UserDumpSerializer(
            instance=user,
            context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False)
    def dump(self, request):
        qs = self.filter_queryset(self.get_queryset())
        paginated_qs = self.paginate_queryset(qs)
        serializer = serializers.UserDumpSerializer(
            instance=paginated_qs,
            many=True,
            context=self.get_serializer_context(),
        )
        return self.get_paginated_response(serializer.data)


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikeDetailSerializer
    queryset = vehicles.models.Bike.objects.all()
    required_permissions = (
        "vehicles.can_list_bikes",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"


# TODO: should external users be allowed to delete existing tags?
class PhysicalTagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,  mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    queryset = vehicles.models.PhysicalTag.objects.all()
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
        return vehicles.models.BikeStatus.objects.all()


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GallerySerializer
    required_permissions = (
        "vehicles.can_list_bikes",
    )
    required_object_permissions = (
        "vehicles.can_edit_bike",
    )

    def get_queryset(self):
        return photologue.models.Gallery.objects.all()


class PictureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PictureSerializer
    required_permissions = (
        "vehicles.can_list_bikes",
    )
    required_object_permissions = (
        "vehicles.can_edit_bike",
    )

    def get_queryset(self):
        return photologue.models.Photo.objects.all()


class BikeObservationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = serializers.BikeObservationSerializer
    required_permissions = (
        "vehiclemonitor.can_list_bike_observation",
    )
    queryset = vehiclemonitor.models.BikeObservation.objects.all()
