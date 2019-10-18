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

from .. import models
from . import serializers

logger = logging.getLogger(__name__)

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class MySegmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    required_permissions = (
        "tracks.can_list_own_segments",
        "tracks.can_delete_own_segments",
    )

    def get_queryset(self):
        return models.Segment.objects.filter(
            track__owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.MyBriefSegmentSerializer
        else:
            result = serializers.MySegmentSerializer
        return result


class MyTrackViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    required_permissions = (
        "tracks.can_list_own_tracks",
        "tracks.can_delete_own_tracks",
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "session_id",
        "is_valid",
    )

    def get_queryset(self):
        return models.Track.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.MyTrackListSerializer
        else:
            result = serializers.MyTrackDetailSerializer
        return result


class TrackViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    required_permissions = (
        "tracks.can_list_tracks",
    )
    queryset = models.Track.objects.all()
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "session_id",
        "is_valid",
    )

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.TrackListSerializer
        else:
            result = serializers.TrackDetailSerializer
        return result


class SegmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.SegmentSerializer
    required_permissions = (
        "tracks.can_list_segments",
    )
    queryset = models.Segment.objects.all()
