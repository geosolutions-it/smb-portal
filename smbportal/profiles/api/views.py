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

from keycloakauth import utils
from keycloakauth.keycloakadmin import get_manager

from .. import models
from . import serializers
from . import pagination

logger = logging.getLogger(__name__)


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


class SmbUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SmbUserSerializer
    queryset = models.SmbUser.objects.all()
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
            profile_model=models.EndUserProfile
        )
        return user

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


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
