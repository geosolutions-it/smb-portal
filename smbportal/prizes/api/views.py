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
from rest_framework import viewsets
from rest_framework.response import Response

from .. import models
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


class MyCurrentCompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserCompetitionDetailSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_queryset(self):
        user_age = getattr(self.request.user.profile, "age")
        if user_age is not None:
            qs = models.CurrentCompetition.objects.filter(
                age_groups__contains=[user_age])
        else:
            qs = models.CurrentCompetition.objects.all()
        return qs

    def get_serializer_context(self):
        """Inject the current user into the serializer context"""
        context = super().get_serializer_context()
        context.update(user=self.request.user)
        return context


class MyCompetitionWonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionWonDetailSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_queryset(self):
        return models.FinishedCompetition.objects.filter(
            winners__user=self.request.user)

    def get_serializer_context(self):
        """Inject the current user into the serializer context"""
        context = super().get_serializer_context()
        context.update(user=self.request.user)
        return context
