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

from rest_framework.decorators import action
from rest_framework import (
    mixins,
    viewsets
)
from rest_framework import status
from rest_framework.response import Response

from .. import models
from .. import utils
from . import serializers

logger = logging.getLogger(__name__)

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionDetailSerializer
    queryset = models.Competition.objects.all()
    required_permissions = (
        "profiles.can_list_competitions",
    )

    def get_serializer_class(self):
        if self.action in ["list", "current_competitions"]:
            result = serializers.CompetitionListSerializer
        else:
            result = serializers.CompetitionDetailSerializer
        return result

    @action(detail=False)
    def current_competitions(self, request):
        qs = models.CurrentCompetition.objects.all()
        filtered = self.filter_queryset(qs)
        page = self.paginate_queryset(filtered)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(filtered, many=True)
            result = Response(serializer.data)
        return result


class MyCurrentCompetitionViewSet(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = serializers.CompetitionParticipantDetailSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_serializer_class(self):
        if self.action == "create":
            result = serializers.CompetitionParticipantRequestSerializer
        else:
            result = self.serializer_class
        return result

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            request=self.request,
            user=self.request.user,
        )
        return context

    def get_queryset(self):
        return models.CompetitionParticipant.objects.filter(
            user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        """
        Reimplemented in order to show the created instance in the response.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        participant = models.CompetitionParticipant.objects.get(
            competition__id=serializer.data["competition_id"],
            user=request.user
        )
        out_serializer = self.serializer_class(
            instance=participant, context={"request": request})
        return Response(
            out_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class MyAvailableCompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionListSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_queryset(self):
        return utils.get_available_competitions(self.request.user)

    def get_serializer_context(self):
        """Inject the current user into the serializer context"""
        context = super().get_serializer_context()
        context.update(user=self.request.user)
        return context


class MyCompetitionWonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionParticipantDetailSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_queryset(self):
        return models.CompetitionParticipant.objects.filter(
            user=self.request.user,
            winner__isnull=False
        )

    def get_serializer_context(self):
        """Inject the current user into the serializer context"""
        context = super().get_serializer_context()
        context.update(user=self.request.user)
        return context
