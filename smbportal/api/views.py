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

import photologue.models
from rest_framework import mixins
from rest_framework import viewsets

import profiles.models
import vehicles.models
from . import serializers

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

    def get_queryset(self):
        return vehicles.models.Bike.objects.filter(owner=self.request.user)


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
    serializer_class = serializers.MyBikeStatusSerializer
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

    def get_object(self):
        return self.get_queryset().get(keycloak__UID=self.kwargs["pk"])


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


class PhysicalTagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializers.PhysicalTagSerializer
    queryset = vehicles.models.PhysicalTag.objects.all()
    required_permissions = (
        "vehicles.can_list_physical_tags",
    )
    required_object_permissions = (
        "vehicles.can_delete_physical_tags",
    )


class BikeStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikeStatusSerializer
    required_permissions = (
        "vehicles.can_list_bike_status",
    )

    def get_queryset(self):
        return vehicles.models.BikeStatus.objects.all()


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GallerySerializer

    def get_queryset(self):
        return photologue.models.Gallery.objects.all()


class PictureViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PictureSerializer

    def get_queryset(self):
        return photologue.models.Photo.objects.all()
