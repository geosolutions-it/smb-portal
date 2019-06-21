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
import django_gamification.models
from rest_framework import viewsets

from . import serializers

logger = logging.getLogger(__name__)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BadgeSerializer
    required_permissions = (
        "profiles.can_list_badges",
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "acquired",
    )
    queryset = django_gamification.models.Badge.objects.all()


class MyBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    required_permissions = (
        "profiles.can_list_own_badges",
    )

    def get_queryset(self):
        return django_gamification.models.Badge.objects.filter(
            interface__smbuser=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.MyMixedBadgesSerializer
        else:
            result = serializers.MyBadgeSerializer
        return result

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            serializer_class = self.get_serializer_class()
            context = self.get_serializer_context()
            qs = self.get_queryset()
            serializer = serializer_class(instance=qs, context=context)
        else:
            serializer = super().get_serializer(*args, **kwargs)
        return serializer


