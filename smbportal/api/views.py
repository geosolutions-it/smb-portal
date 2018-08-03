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

from keycloakauth import utils
from keycloakauth.keycloakadmin import get_manager
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
    serializer_class = serializers.MyUserSerializer
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
