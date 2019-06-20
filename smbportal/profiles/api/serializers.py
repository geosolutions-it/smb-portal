#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Serializers for the smbportal REST API"""

import logging

from avatar.templatetags.avatar_tags import avatar_url
from django.db.models import OuterRef
from django.db.models import Subquery
import django_gamification.models as gm
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import tracks.utils
from badges.api.serializers import (
    BriefBadgeSerializer,
    MyBriefBadgeSerializer
)
from vehicles.api.serializers import BikeDetailSerializer

from .. import models
from .fields import SmbUserHyperlinkedIdentityField

logger = logging.getLogger(__name__)


class SmbUserSerializer(serializers.HyperlinkedModelSerializer):
    url = SmbUserHyperlinkedIdentityField(
        view_name="api:users-detail",
    )
    uuid = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()
    acquired_badges = serializers.SerializerMethodField()
    next_badges = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_uuid(self, obj):
        return obj.keycloak.UID

    def get_avatar(self, obj):
        return avatar_url(obj)

    def get_acquired_badges(self, obj):
        if obj.gamification_interface is None:
            result = []
        else:
            badges = obj.gamification_interface.badge_set.filter(acquired=True)
            serializer = BriefBadgeSerializer(
                instance=badges,
                context=self.context,
                many=True
            )
            result = serializer.data
        return result

    def get_next_badges(self, obj):
        if obj.gamification_interface is None:
            result = []
        else:
            unacquired = gm.Badge.objects.filter(
                acquired=False,
                interface__smbuser=obj,
                category=OuterRef("pk")
            )
            next_badges_ids = gm.Category.objects.annotate(
                next_badge=Subquery(unacquired.values("pk")[:1])
            ).values_list("next_badge", flat=True)
            qs = gm.Badge.objects.filter(
                pk__in=next_badges_ids).order_by("name")
            serializer = BriefBadgeSerializer(
                instance=qs,
                context=self.context,
                many=True
            )
            result = serializer.data
        return result


    def get_profile(self, obj):
        profile_type = self.get_profile_type(obj)
        if profile_type is not None:
            serializer_class = self._get_profile_serializer_class(profile_type)
            serializer = serializer_class(
                instance=obj.profile,
                context=self.context
            )
            result = serializer.data
        else:
            result = None
        return result

    def get_profile_type(self, obj):
        return type(obj.profile).__name__.lower() if obj.profile else None

    def _get_profile_serializer_class(self, profile_type):
        return {
            "privilegeduserprofile": (
                PrivilegedUserProfileSerializer),
        }.get(profile_type, EndUserProfileSerializer)

    class Meta:
        model = models.SmbUser
        fields = (
            "url",
            "uuid",
            "username",
            "email",
            "date_joined",
            "language_preference",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
            "avatar",
            "acquired_badges",
            "next_badges",
        )


class MyUserSerializer(SmbUserSerializer):
    username = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    language_preference = serializers.CharField(required=False)
    url = serializers.SerializerMethodField()
    total_health_benefits = serializers.SerializerMethodField()
    total_emissions = serializers.SerializerMethodField()
    total_distance_km = serializers.SerializerMethodField()
    total_travels = serializers.SerializerMethodField()

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.accepted_terms_of_service = validated_data.get(
            "accepted_terms_of_service", instance.accepted_terms_of_service)
        instance.language_preference = validated_data.get(
            "language_preference", instance.language_preference)
        # The profile-related fields are fetched from `initial_data` instead
        # `validated_data` intentionally. Since their representation
        # is being created using `serializers.SerializerMethodField`, they
        # are supposed to be readonly, and thus rest-framework does not use
        # them for data updates (so they do not show up in `validated_data`).
        # This is likely a hacky way to support different models under the
        # same `profile` attribute name
        initial_data = getattr(self, "initial_data", {})
        profile_type = initial_data.get("profile_type")
        profile_data = initial_data.get("profile")
        if profile_data is not None:
            self._update_profile(instance, profile_data, profile_type)
        instance.save()
        return instance

    def _update_profile(self, instance, profile_data, profile_type):
        """Update the nested `profile` resource"""
        profile_type_matches = self.get_profile_type(instance) == profile_type
        is_correct_profile_type = (
            (profile_type_matches and profile_type is not None) or
            (profile_type is None)
        )
        if not is_correct_profile_type:
            raise ValidationError({"profile_type": "incorrect value"})
        profile_serializer_context = self.context.copy()
        profile_serializer_context.update({
            "user": instance
        })
        profile_serializer_class = self._get_profile_serializer_class(
            profile_type)
        current_profile = instance.profile
        if current_profile is None:
            profile_serializer = profile_serializer_class(
                data=profile_data,
                context=profile_serializer_context
            )
        else:
            profile_serializer = profile_serializer_class(
                instance=current_profile,
                data=profile_data,
                context=profile_serializer_context,
                partial=True
            )
        profile_serializer.is_valid(raise_exception=True)
        user_profile = profile_serializer.save()
        return user_profile

    def get_url(self, obj):
        return reverse("api:my-user", request=self.context.get("request"))

    def get_acquired_badges(self, obj):
        if obj.gamification_interface is None:
            result = []
        else:
            badges = obj.gamification_interface.badge_set.filter(
                acquired=True).order_by("name")
            serializer = MyBriefBadgeSerializer(
                instance=badges,
                context=self.context,
                many=True
            )
            result = serializer.data
        return result

    def get_next_badges(self, obj):
        if obj.gamification_interface is None:
            result = []
        else:
            unacquired = gm.Badge.objects.filter(
                acquired=False,
                interface__smbuser=obj,
                category=OuterRef("pk")
            )
            next_badges_ids = gm.Category.objects.annotate(
                next_badge=Subquery(unacquired.values("pk")[:1])
            ).values_list("next_badge", flat=True)
            qs = gm.Badge.objects.filter(
                pk__in=next_badges_ids).order_by("name")
            serializer = MyBriefBadgeSerializer(
                instance=qs,
                context=self.context,
                many=True
            )
            result = serializer.data
        return result

    def get_total_health_benefits(self, obj):
        return tracks.utils.get_aggregated_data(
            "health",
            segment_filters={"track__owner": obj}
        )

    def get_total_emissions(self, obj):
        return tracks.utils.get_aggregated_data(
            "emissions",
            segment_filters={"track__owner": obj}
        )

    def get_total_distance_km(self, obj):
        return tracks.utils.get_total_distance_by_vehicle_type(obj)

    def get_total_travels(self, obj):
        return tracks.utils.get_total_travels_by_vehicle_type(obj)

    class Meta:
        model = models.SmbUser
        fields = (
            "accepted_terms_of_service",
            "url",
            "uuid",
            "username",
            "email",
            "date_joined",
            "language_preference",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
            "avatar",
            "acquired_badges",
            "next_badges",
            "total_health_benefits",
            "total_emissions",
            "total_distance_km",
            "total_travels",
        )


class UserDumpSerializer(SmbUserSerializer):
    """Produce a User, its vehicles and Tags"""

    vehicles = serializers.SerializerMethodField()

    def get_vehicles(self, obj):
        serializer = BikeDetailSerializer(
            instance=obj.bikes.all(),
            many=True,
            context=self.context
        )
        return serializer.data

    class Meta:
        model = models.SmbUser
        fields = (
            "url",
            "uuid",
            "username",
            "email",
            "date_joined",
            "language_preference",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
            "vehicles",
            "avatar",
            "acquired_badges",
        )


class EndUserProfileSerializer(serializers.ModelSerializer):
    date_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.EndUserProfile
        fields = (
            "gender",
            "age",
            "phone_number",
            "bio",
            "date_updated",
            "occupation",
        )

    def create(self, validated_data):
        return models.EndUserProfile.objects.create(
            user=self.context["user"],
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.gender = validated_data.get("gender", instance.gender)
        instance.age = validated_data.get("age", instance.gender)
        instance.phone_number = validated_data.get(
            "phone_number", instance.gender)
        instance.bio = validated_data.get("bio", instance.gender)
        instance.occupation = validated_data.get(
            "occupation", instance.occupation)
        instance.save()
        return instance


class PrivilegedUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PrivilegedUserProfile
        fields = ()
