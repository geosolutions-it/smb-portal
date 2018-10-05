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

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_gis.pagination import GeoJsonPagination
import django_gamification.models

from keycloakauth import utils
from keycloakauth.keycloakadmin import get_manager
import prizes.models
import profiles.models
import profiles.views
import tracks.models
import vehicles.models
import vehiclemonitor.models
from . import pagination
from . import serializers
from . import filters

logger = logging.getLogger(__name__)

# TODO: Specify permission_classes for all views
# FIXME: account for different user profiles


class MyUserViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.MyUserSerializer
    required_permissions = (
        "profiles.is_authenticated",
    )

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, obj=user.profile)
        return user

    def perform_update(self, serializer):
        """Save any modifications to the user object

        In case of profile generation, be sure to communicate with keycloak
        in order to setup correct group memberships

        """

        user = serializer.save()
        _update_group_memberships(user)


class MyBikeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyBikeDetailSerializer
    required_permissions = (
        "vehicles.can_list_own_bikes",
        "vehicles.can_create_bike",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"

    def get_queryset(self):
        return vehicles.models.Bike.objects.filter(owner=self.request.user)


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
        return vehiclemonitor.models.BikeObservation.objects.filter(
            bike__owner=self.request.user)


class MyPhysicalTagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.MyPhysicalTagSerializer
    required_permissions = (
        "vehicles.can_list_own_physical_tags",
    )
    lookup_field = "epc"

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


class MySegmentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    required_permissions = (
        "tracks.can_list_own_segments",
        "tracks.can_delete_own_segments",
    )

    def get_queryset(self):
        return tracks.models.Segment.objects.filter(
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
    )

    def get_queryset(self):
        return tracks.models.Track.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.MyTrackListSerializer
        else:
            result = serializers.MyTrackDetailSerializer
        return result


class SmbUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SmbUserSerializer
    queryset = profiles.models.SmbUser.objects.all()
    required_permissions = (
        "profiles.can_list_users",
        "profiles.can_delete_user",
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "email",
        "username",
    )
    lookup_field = "uuid"
    pagination_class = pagination.SmbUserDumpPageNumberPagination

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

    def perform_destroy(self, instance):
        manager = get_manager(
            settings.KEYCLOAK["base_url"],
            settings.KEYCLOAK["realm"],
            settings.KEYCLOAK["client_id"],
            settings.KEYCLOAK["admin_username"],
            settings.KEYCLOAK["admin_password"],
        )
        utils.delete_user(
            instance.username,
            manager
        )

    @action(methods=["POST"], detail=False)
    def create_end_user(self, request):
        """Create a new user with the `end user` profile.

        The user is created both on the portal and on keycloak

        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create_end_user(serializer)
        output_serializer = self.get_serializer_class()(
            instance=user,
            context={"request": request}
        )
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(output_serializer.data)
        )

    def perform_create_end_user(self, serializer):
        group_path = settings.KEYCLOAK[
            "group_mappings"][settings.END_USER_PROFILE][0]
        manager = get_manager(
            settings.KEYCLOAK["base_url"],
            settings.KEYCLOAK["realm"],
            settings.KEYCLOAK["client_id"],
            settings.KEYCLOAK["admin_username"],
            settings.KEYCLOAK["admin_password"],
        )
        user = utils.create_user(
            username=serializer.validated_data.get("username"),
            email=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
            group_path=group_path,
            keycloak_manager=manager,
            profile_model=profiles.models.EndUserProfile
        )
        return user

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BikeDetailSerializer
    queryset = vehicles.models.Bike.objects.all()
    required_permissions = (
        "vehicles.can_list_bikes",
    )
    filter_class = filters.BikeFilterSet
    lookup_field = "short_uuid"


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


class BikeObservationViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = serializers.BikeObservationSerializer
    required_permissions = (
        "vehiclemonitor.can_list_bike_observation",
    )
    queryset = vehiclemonitor.models.BikeObservation.objects.all()


class TrackViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    required_permissions = (
        "tracks.can_list_tracks",
    )
    queryset = tracks.models.Track.objects.all()
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "session_id",
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
    queryset = tracks.models.Segment.objects.all()


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
    serializer_class = serializers.MyBadgeSerializer
    required_permissions = (
        "profiles.can_list_own_badges",
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_fields = (
        "acquired",
    )

    def get_queryset(self):
        return django_gamification.models.Badge.objects.filter(
            interface__smbuser=self.request.user)


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionDetailSerializer
    queryset = prizes.models.Competition.objects.all()
    required_permissions = (
        "profiles.can_list_competitions",
    )

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.CompetitionListSerializer
        else:
            result = serializers.CompetitionDetailSerializer
        return result

    @action(detail=False)
    def current_competitions(self, request):
        qs = prizes.models.CurrentCompetition.objects.all()
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
            qs = prizes.models.CurrentCompetition.objects.filter(
                age_groups__contains=[user_age])
        else:
            qs = prizes.models.CurrentCompetition.objects.all()
        return qs

    def get_serializer_context(self):
        """Inject the current user into the serializer context"""
        context = super().get_serializer_context()
        context.update(user=self.request.user)
        return context


class MyCompetitionWonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CompetitionDetailSerializer
    required_permissions = (
        "profiles.can_list_own_competitions",
    )

    def get_queryset(self):
        return prizes.models.FinishedCompetition.objects.filter(
            winners__user=self.request.user)


def _update_group_memberships(user):
    manager = get_manager(
        settings.KEYCLOAK["base_url"],
        settings.KEYCLOAK["realm"],
        settings.KEYCLOAK["client_id"],
        settings.KEYCLOAK["admin_username"],
        settings.KEYCLOAK["admin_password"],
    )
    user_groups = manager.get_user_groups(user.keycloak.UID)
    logger.debug("updating user group memberships...")
    profile_name = (user.profile.__class__.__name__.lower() if
                    user.profile is not None else None)
    keycloak_group_name = {
        "enduserprofile": settings.END_USER_PROFILE,
        "privilegeduserprofile": settings.PRIVILEGED_USER_PROFILE,
    }.get(profile_name or "")
    utils.update_user_groups(
        user=user,
        user_profile=keycloak_group_name,
        current_keycloak_groups=[g["name"] for g in user_groups]
    )
