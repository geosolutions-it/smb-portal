#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import photologue.models
from rest_framework import viewsets
from rest_framework import mixins

import profiles.models
import vehicles.models
from . import serializers

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class MyUserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.SmbUserSerializer

    def get_object(self):
        return self.request.user


class MyBikeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BikeDetailSerializer
    required_permissions = (
        "vehicles.can_create_bike",
    )

    def get_queryset(self):
        return vehicles.models.Bike.objects.filter(owner=self.request.user)


class MyPhysicalTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    required_permissions = (
        "vehicles.can_create_physical_tag",
    )

    def get_queryset(self):
        return vehicles.models.PhysicalTag.objects.filter(
            bike__owner=self.request.user)


class SmbUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SmbUserSerializer
    queryset = profiles.models.SmbUser.objects.all()
    required_permissions = (
        "profiles.can_list_users",
    )


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = vehicles.models.Bike.objects.all()
    required_permissions = (
        "vehicles.can_list_bikes",
    )

    def get_serializer_class(self):
        if self.action == "retrieve":
            serializer_class = serializers.BikeDetailSerializer
        else:
            serializer_class = serializers.BikeListSerializer
        return serializer_class

    def retrieve(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)


class PhysicalTagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    queryset = vehicles.models.PhysicalTag.objects.all()
    required_permissions = (
        "vehicles.can_list_physical_tags",
    )


class BikePossessionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikePossessionHistorySerializer

    def get_queryset(self):
        return vehicles.models.BikePossessionHistory.objects.all()


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GallerySerializer

    def get_queryset(self):
        return photologue.models.Gallery.objects.all()


class PictureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PictureSerializer

    def get_queryset(self):
        return photologue.models.Photo.objects.all()
