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

import profiles.models
import vehicles.models
from . import serializers

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles

class SmbUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.SmbUserSerializer

    def get_queryset(self):
        return profiles.models.SmbUser.objects.all()


class BikeViewSet(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        return vehicles.models.Bike.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            serializer_class = serializers.BikeDetailSerializer
        else:
            serializer_class = serializers.BikeListSerializer
        return serializer_class


class PhysicalTagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhysicalTagSerializer

    def get_queryset(self):
        return vehicles.models.PhysicalTag.objects.all()


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
