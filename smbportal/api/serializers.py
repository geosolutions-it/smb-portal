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

from rest_framework.reverse import reverse
import photologue.models
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

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
    password = serializers.CharField(write_only=True)

    def get_uuid(self, obj):
        return obj.keycloak.UID

    def get_profile(self, obj):
        if obj.profile is not None:
            serializer_class = {
                "enduserprofile": EndUserProfileSerializer,
                "privilegeduserprofile": (
                    PrivilegedUserProfileSerializer),
            }.get(obj.profile.__class__.__name__.lower())
            print("class: {}".format(obj.profile.__class__))
            print("class_name: {}".format(obj.profile.__class__.__name__))
            print("serializer class: {}".format(serializer_class))
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

    class Meta:
        model = profiles.models.SmbUser
        fields = (
            "url",
            "uuid",
            "username",
            "password",
            "email",
            "date_joined",
            "language_preference",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
        )


class MyUserSerializer(SmbUserSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse("api:my-user", request=self.context.get("request"))

    class Meta:
        model = profiles.models.SmbUser
        fields = (
            "url",
            "uuid",
            "username",
            "password",
            "email",
            "date_joined",
            "language_preference",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
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
            "vehicles"
        )


class EndUserProfileSerializer(serializers.ModelSerializer):

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
