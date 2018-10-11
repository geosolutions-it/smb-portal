#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
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
from django.template import Context
from django.template import Engine
import django_gamification.models as gm
from rest_framework.reverse import reverse
import photologue.models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.serializers import GeoFeatureModelSerializer

import prizes.models
import profiles.models
import tracks.models
import tracks.utils
import vehicles.models
import vehiclemonitor.models

logger = logging.getLogger(__name__)


class SmbUserHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """Custom serializer field to support showing a custom id for ``SmbUser``

    This field allows using the keycloak UUID as the user's identity field in
    the API

    """

    def get_url(self, obj, view_name, request, format):
        return reverse(
            view_name,
            kwargs={
                "uuid": obj.keycloak.UID
            },
            request=request,
            format=format
        )


class SmbUserHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """Custom serializer field to support showing a custom id for ``SmbUser``

    This field allows using the keycloak UUID as the related attribute when
    referencing user model from other models in the API

    """

    def get_url(self, obj, view_name, request, format):
        return reverse(
            view_name,
            kwargs={
                "uuid": obj.keycloak.UID
            },
            request=request,
            format=format
        )

    def get_object(self, view_name, view_args, view_kwargs):
        return self.get_queryset().get(keycloak__UID=view_kwargs.get("pk"))

    def use_pk_only_optimization(self):
        return False


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
        model = profiles.models.SmbUser
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
        model = profiles.models.SmbUser
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
        model = profiles.models.SmbUser
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
        model = profiles.models.EndUserProfile
        fields = (
            "gender",
            "age",
            "phone_number",
            "bio",
            "date_updated",
            "occupation",
        )

    def create(self, validated_data):
        return profiles.models.EndUserProfile.objects.create(
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
        model = profiles.models.PrivilegedUserProfile
        fields = ()


class BikeListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bikes-detail",
        lookup_field="short_uuid",
    )
    owner = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:tags-detail",
        many=True,
        read_only=True,
        lookup_field="epc"
    )
    current_status = serializers.SerializerMethodField()

    def get_current_status(self, obj):
        current_status = obj.get_current_status()
        return {
            "lost": current_status.lost,
            "url": reverse(
                "api:bike-statuses-detail",
                kwargs={
                    "pk": current_status.pk
                },
                request=self.context.get("request")
            )
        }

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "short_uuid",
            "nickname",
            "owner",
            "tags",
            "current_status",
            "last_update",
        )


class BikeDetailSerializer(BikeListSerializer):
    pictures = serializers.SerializerMethodField()

    def get_pictures(self, bike):
        serializer = PictureSerializer(
            instance=bike.picture_gallery.photos.all(),
            context=self.context,
            many=True
        )
        return [item["image"] for item in serializer.data]

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "short_uuid",
            "owner",
            "pictures",
            "tags",
            "last_update",
            "bike_type",
            "gear",
            "brake",
            "nickname",
            "brand",
            "model",
            "color",
            "saddle",
            "has_basket",
            "has_cargo_rack",
            "has_bags",
            "other_details",
            "current_status",
        )


class MyBikeDetailSerializer(BikeDetailSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-bikes-detail",
        lookup_field="short_uuid",
    )
    owner = serializers.SerializerMethodField()
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:my-tags-detail",
        many=True,
        read_only=True,
        lookup_field="epc"
    )

    def get_owner(self, obj):
        return reverse("api:my-user", request=self.context.get("request"))

    def get_current_status(self, obj):
        current_status = obj.get_current_status()
        return {
            "lost": current_status.lost,
            "url": reverse(
                "api:my-bike-statuses-detail",
                kwargs={
                    "pk": current_status.pk
                },
                request=self.context.get("request")
            )
        }

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "short_uuid",
            "owner",
            "pictures",
            "tags",
            "last_update",
            "bike_type",
            "gear",
            "brake",
            "nickname",
            "brand",
            "model",
            "color",
            "saddle",
            "has_basket",
            "has_cargo_rack",
            "has_bags",
            "other_details",
            "current_status",
        )


class PhysicalTagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:tags-detail",
        lookup_field="epc",
        lookup_url_kwarg="epc",
    )
    bike = serializers.SlugRelatedField(
        slug_field="short_uuid",
        queryset=vehicles.models.Bike.objects.all()
    )
    bike_url = serializers.HyperlinkedRelatedField(
        source="bike",
        read_only=True,
        view_name="api:bikes-detail",
        lookup_field="short_uuid",
    )

    class Meta:
        model = vehicles.models.PhysicalTag
        fields = (
            "url",
            "epc",
            "bike",
            "bike_url",
            "creation_date",
        )


class MyPhysicalTagSerializer(PhysicalTagSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-tags-detail",
        lookup_field="epc",
        lookup_url_kwarg="epc",
    )

    bike_url = serializers.HyperlinkedRelatedField(
        source="bike",
        read_only=True,
        view_name="api:my-bikes-detail",
        lookup_field="short_uuid",
    )

    class Meta:
        model = vehicles.models.PhysicalTag
        fields = (
            "url",
            "epc",
            "bike",
            "bike_url",
            "creation_date",
        )


class BikeStatusSerializer(GeoFeatureModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bike-statuses-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        lookup_field="short_uuid",
        queryset=vehicles.models.Bike.objects.all()
    )

    class Meta:
        model = vehicles.models.BikeStatus
        geo_field = "position"
        fields = (
            "url",
            "id",
            "bike",
            "lost",
            "creation_date",
            "details",
        )

    def __init__(self, *args, **kwargs):
        """Initialize serializer

        This method is reimplemented in order to provide the ability to remove
        fields dynamically, as documented at:

            http://www.django-rest-framework.org/api-guide/
                serializers/#dynamically-modifying-fields

        This feature is handy since this serializer is used both in a
        standalone resource view and also as part of the representation for
        bikes. In the second case it is unnecessary to include the bike
        URL again.

        """

        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed_fields = set(fields)
            existing_fields = set(self.fields)
            for field_name in existing_fields - allowed_fields:
                self.fields.pop(field_name)


class MyBikeStatusSerializer(BikeStatusSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-bike-statuses-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:my-bikes-detail",
        lookup_field="short_uuid",
        queryset=vehicles.models.Bike.objects.all()
    )

    class Meta:
        model = vehicles.models.BikeStatus
        geo_field = "position"
        fields = (
            "url",
            "id",
            "bike",
            "lost",
            "creation_date",
            "details",
        )


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:picture-galleries-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        lookup_field="short_uuid",
        read_only=True
    )
    photos = serializers.HyperlinkedRelatedField(
        view_name="api:pictures-detail",
        many=True,
        read_only=True,
    )

    class Meta:
        model = photologue.models.Gallery
        fields = (
            "url",
            "id",
            "bike",
            "title",
            "photos",
        )


class PictureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = photologue.models.Photo
        fields = (
            "id",
            "image",
        )


class BikeObservationSerializer(GeoFeatureModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bike-observations-detail",
    )
    bike = serializers.SlugRelatedField(
        slug_field="short_uuid",
        queryset=vehicles.models.Bike.objects.all()
    )
    bike_url = serializers.HyperlinkedRelatedField(
        source="bike",
        read_only=True,
        view_name="api:bikes-detail",
        lookup_field="short_uuid",
    )

    class Meta:
        model = vehiclemonitor.models.BikeObservation
        geo_field = "position"
        fields = (
            "url",
            "id",
            "bike",
            "bike_url",
            "reporter_id",
            "reporter_type",
            "reporter_name",
            "address",
            "created_at",
            "observed_at",
            "details",
        )


class MyBikeObservationSerializer(BikeObservationSerializer):
    bike = serializers.SlugRelatedField(
        slug_field="short_uuid",
        queryset=vehicles.models.Bike.objects.all()
    )
    bike_url = serializers.HyperlinkedRelatedField(
        source="bike",
        read_only=True,
        view_name="api:my-bikes-detail",
        lookup_field="short_uuid",
    )

    class Meta:
        model = vehiclemonitor.models.BikeObservation
        geo_field = "position"
        fields = (
            "id",
            "bike",
            "bike_url",
            "reporter_id",
            "reporter_type",
            "reporter_name",
            "address",
            "created_at",
            "observed_at",
            "details",
        )


class TrackListSerializer(serializers.ModelSerializer):
    owner = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    url = serializers.HyperlinkedIdentityField(view_name="api:tracks-detail")
    segments = serializers.SerializerMethodField()
    vehicle_types = serializers.SerializerMethodField()
    emissions = serializers.DictField(source="aggregated_emissions")
    costs = serializers.DictField(source="aggregated_costs")
    health = serializers.DictField(source="aggregated_health")
    duration_minutes = serializers.FloatField(source="duration")
    length_meters = serializers.FloatField(source="length")

    def get_vehicle_types(self, obj):
        unique_types = set(obj.segments.values_list("vehicle_type", flat=True))
        return list(unique_types)

    def get_segments(self, obj):
        serializer = BriefSegmentSerializer(
            instance=obj.segments, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = tracks.models.Track
        fields = (
            "id",
            "url",
            "session_id",
            "owner",
            "segments",
            "start_date",
            "end_date",
            "duration_minutes",
            "length_meters",
            "vehicle_types",
            "emissions",
            "costs",
            "health",
        )


class MyTrackListSerializer(TrackListSerializer):
    owner = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-tracks-detail")

    def get_owner(self, obj):
        return reverse("api:my-user", request=self.context.get("request"))

    def get_segments(self, obj):
        serializer = MyBriefSegmentSerializer(
            instance=obj.segments, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = tracks.models.Track
        fields = (
            "id",
            "url",
            "session_id",
            "owner",
            "segments",
            "start_date",
            "end_date",
            "duration_minutes",
            "length_meters",
            "vehicle_types",
            "emissions",
            "costs",
            "health",
        )


class TrackDetailSerializer(TrackListSerializer):
    """Serializer for a Track's detail endpoint

    Similar to TrackListSerializer, with the following enhancements:

    - `emissions`, `costs` and `health` fields **total values**
    - `segments` field returns the full representation for each segment

    """

    emissions = serializers.DictField(source="aggregated_emissions")
    costs = serializers.DictField(source="aggregated_costs")
    health = serializers.DictField(source="aggregated_health")

    def get_segments(self, obj):
        serializer = SegmentSerializer(
            instance=obj.segments, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = tracks.models.Track
        fields = (
            "id",
            "url",
            "session_id",
            "owner",
            "segments",
            "start_date",
            "end_date",
            "duration_minutes",
            "length_meters",
            "vehicle_types",
            "emissions",
            "costs",
            "health",
        )


class MyTrackDetailSerializer(TrackDetailSerializer):
    owner = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-tracks-detail")

    def get_owner(self, obj):
        return reverse("api:my-user", request=self.context.get("request"))

    def get_segments(self, obj):
        serializer = MySegmentSerializer(
            instance=obj.segments, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = tracks.models.Track
        fields = (
            "id",
            "url",
            "session_id",
            "owner",
            "segments",
            "start_date",
            "end_date",
            "duration_minutes",
            "length_meters",
            "vehicle_types",
            "emissions",
            "costs",
            "health",
        )


class SegmentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:segments-detail")
    geom = serializers.SerializerMethodField()
    emissions = serializers.SerializerMethodField()
    costs = serializers.SerializerMethodField()
    health = serializers.SerializerMethodField()
    track = serializers.HyperlinkedRelatedField(
        view_name="api:tracks-detail",
        read_only=True
    )

    def get_geom(self, obj):
        return obj.geom.geojson

    def get_emissions(self, obj):
        serializer = EmissionSerializer(
            instance=obj.emission, context=self.context)
        return serializer.data

    def get_costs(self, obj):
        serializer = CostSerializer(
            instance=obj.cost, context=self.context)
        return serializer.data

    def get_health(self, obj):
        serializer = HealthSerializer(
            instance=obj.health, context=self.context)
        return serializer.data

    class Meta:
        model = tracks.models.Segment
        fields = (
            "id",
            "url",
            "track",
            "geom",
            "start_date",
            "end_date",
            "vehicle_type",
            "vehicle_id",
            "emissions",
            "costs",
            "health",
        )


class MySegmentSerializer(SegmentSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-segments-detail"
    )
    track = serializers.HyperlinkedRelatedField(
        view_name="api:my-tracks-detail",
        read_only=True
    )

    class Meta:
        model = tracks.models.Segment
        fields = (
            "id",
            "url",
            "track",
            "geom",
            "start_date",
            "end_date",
            "vehicle_type",
            "vehicle_id",
            "emissions",
            "costs",
            "health",
        )


class BriefSegmentSerializer(SegmentSerializer):
    class Meta:
        model = tracks.models.Segment
        fields = (
            "id",
            "url",
            "geom"
        )


class MyBriefSegmentSerializer(MySegmentSerializer):
    class Meta:
        model = tracks.models.Segment
        fields = (
            "id",
            "url",
            "geom"
        )


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tracks.models.Emission
        fields = (
            "so2",
            "so2_saved",
            "nox",
            "nox_saved",
            "co2",
            "co2_saved",
            "co",
            "co_saved",
            "pm10",
            "pm10_saved",
        )


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = tracks.models.Cost
        fields = (
            "fuel_cost",
            "time_cost",
            "depreciation_cost",
            "operation_cost",
            "total_cost",
        )


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = tracks.models.Health
        fields = (
            "calories_consumed",
            "benefit_index",
        )


class BadgeSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    user = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name="api:badges-detail",
    )
    next_badge = serializers.HyperlinkedRelatedField(
        view_name="api:badges-detail",
        queryset=gm.Badge.objects.all()
    )

    def get_user(self, obj):
        user = obj.interface.smbuser_set.first()
        return reverse(
            "api:users-detail",
            kwargs={"uuid": user.keycloak.UID},
            request=self.context.get("request")
        )

    class Meta:
        model = gm.Badge
        fields = (
            "id",
            "url",
            "name",
            "user",
            "acquired",
            "description",
            "category",
            "next_badge",
        )


class BriefBadgeSerializer(BadgeSerializer):
    class Meta:
        model = gm.Badge
        fields = (
            "name",
            "url",
        )


class MyBadgeSerializer(BadgeSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-badges-detail",
    )
    next_badge = serializers.HyperlinkedRelatedField(
        view_name="api:my-badges-detail",
        queryset=gm.Badge.objects.all()
    )

    class Meta:
        model = gm.Badge
        fields = (
            "id",
            "url",
            "name",
            "acquired",
            "description",
            "category",
            "next_badge",
        )


class MyMixedBadgesSerializer(serializers.BaseSerializer):

    def to_representation(self, user_badges):
        """Return a representation of all relevant badges

        Relevant badges are:

        1. Badges that have already been acquired
        2. Next badges to acquire, after the ones that have been acquired
           already (example: badge2, if badge1 has been acquired already)
        3. First unacquired badges of each category

        """

        unacquired_firsts = self._get_unacquired_category_first_badges(
            user_badges)
        acquired = list(user_badges.filter(acquired=True).order_by("name"))
        next_ = [b.next_badge for b in acquired if b.next_badge is not None]
        leaf_next = [b for b in next_ if b not in acquired]
        consolidated = set(
            unacquired_firsts).union(set(acquired)).union(set(leaf_next))
        sorted_badges = sorted(consolidated, key=lambda b: b.name)
        badge_serializer = MyBadgeSerializer(
            instance=sorted_badges, many=True, context=self.context)
        return badge_serializer.data

    def _get_unacquired_category_first_badges(self, badges):
        """Return a list with the first unacquired badge of each category"""
        unacquired_firsts = []
        for badge in badges.filter(acquired=False).order_by("name"):
            cat_names = [b.category for b in unacquired_firsts]
            if badge.category not in cat_names:
                unacquired_firsts.append(badge)
        return unacquired_firsts


class MyBriefBadgeSerializer(MyBadgeSerializer):
    class Meta:
        model = gm.Badge
        fields = (
            "name",
            "url",
            "acquired",
        )


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = prizes.models.Sponsor
        fields = (
            "name",
            "logo",
            "url",
        )


class CompetitionRankingSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        criteria = instance[1]
        result = {
            "username": instance[0].username
        }
        result.update(
            {criterium.value: score for criterium, score in criteria.items()})
        return result


class PrizeSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer()

    class Meta:
        model = prizes.models.Prize
        fields = (
            "name",
            "description",
            "image",
            "url",
            "sponsor"
        )


class CompetitionPrizeSerializer(serializers.ModelSerializer):
    winner_description = serializers.SerializerMethodField()
    prize = PrizeSerializer()

    def get_winner_description(self, obj):
        engine = Engine.get_default()
        string_template = obj.prize_attribution_template
        try:
            rank = obj.competition.winners.get(user=self.context["user"]).rank
        except prizes.models.Winner.DoesNotExist:
            result = string_template
        else:
            score = obj.competition.get_user_score(self.context["user"])
            formatted_score = ", ".join(
                "{}: {:0.3f}".format(criterium.value, value) for
                criterium, value in score.items()
            )
            context = Context({
                "rank": rank,
                "score": formatted_score,
            })
            if "humanize" not in string_template:
                string_template = "{% load humanize %}" + string_template
            template = engine.from_string(string_template)
            result = template.render(context)
        return result

    class Meta:
        model = prizes.models.CompetitionPrize
        fields = (
            "winner_description",
            "prize",
            "user_rank",
        )


class CompetitionListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:competitions-detail",
    )

    class Meta:
        model = prizes.models.Competition
        fields = (
            "id",
            "url",
            "name",
            "description",
            "age_groups",
            "start_date",
            "end_date",
            "criteria",
        )


class CompetitionDetailSerializer(CompetitionListSerializer):
    leaderboard = serializers.SerializerMethodField()
    prizes = CompetitionPrizeSerializer(
        many=True,
        source="competitionprize_set",
    )

    def get_leaderboard(self, obj):
        board = obj.get_leaderboard()
        serializer = CompetitionRankingSerializer(instance=board, many=True)
        return serializer.data

    class Meta:
        model = prizes.models.Competition
        fields = (
            "id",
            "url",
            "name",
            "description",
            "age_groups",
            "start_date",
            "end_date",
            "criteria",
            "winner_threshold",
            "leaderboard",
            "prizes",
        )


class UserCompetitionDetailSerializer(CompetitionDetailSerializer):
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        score = obj.get_user_score(self.context["user"])
        return {criterium.value: value for criterium, value in  score.items()}

    class Meta:
        model = prizes.models.CurrentCompetition
        fields = (
            "id",
            "url",
            "name",
            "description",
            "age_groups",
            "start_date",
            "end_date",
            "criteria",
            "winner_threshold",
            "score",
            "leaderboard",
            "prizes",
        )


class CompetitionWonDetailSerializer(CompetitionDetailSerializer):
    score = serializers.SerializerMethodField()
    # winner_description = serializers.SerializerMethodField()

    def get_score(self, obj):
        score = obj.get_user_score(self.context["user"])
        return {criterium.value: value for criterium, value in  score.items()}

    # def get_winner_description(self, obj):
    #     engine = Engine.get_default()
    #     rank = obj.winners.get(user=self.context["user"]).rank
    #     score = obj.get_user_score(self.context["user"])
    #     formatted_score = ", ".join(
    #         "{}: {:0.3f}".format(criterium.value, value) for
    #         criterium, value in score.items()
    #     )
    #     context = Context({
    #         "rank": rank,
    #         "score": formatted_score,
    #     })
    #     competition_prizes = obj.competitionprize_set.filter(
    #         user_rank__in=[rank, None])
    #     result = []
    #     for competition_prize in competition_prizes:
    #         string_template = competition_prize.prize_attribution_template
    #         if "humanize" not in string_template:
    #             string_template = "{% load humanize %}" + string_template
    #         template = engine.from_string(string_template)
    #         result.append(template.render(context))
    #     return result


    class Meta:
        model = prizes.models.CurrentCompetition
        fields = (
            "id",
            "url",
            "name",
            "description",
            "age_groups",
            "start_date",
            "end_date",
            "criteria",
            "winner_threshold",
            "score",
            # "winner_description",
            "leaderboard",
            "prizes",
        )
