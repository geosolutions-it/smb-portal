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

    def get_uuid(self, obj):
        return obj.keycloak.UID

    def get_profile(self, obj):
        if obj.profile is not None:
            profile_class = type(obj.profile)
            serializer_class = {
                profiles.models.EndUserProfile: EndUserProfileSerializer,
                profiles.models.PrivilegedUserProfile: (
                    PrivilegedUserProfileSerializer),
            }.get(profile_class)
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
    picture_gallery = serializers.HyperlinkedRelatedField(
        view_name="api:picture-galleries-detail",
        read_only=True
    )
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
            "picture_gallery",
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
    url = serializers.HyperlinkedIdentityField(
        view_name="api:pictures-detail",
    )
    galleries = serializers.HyperlinkedRelatedField(
        view_name="api:picture-galleries-detail",
        many=True,
        read_only=True
    )

    class Meta:
        model = photologue.models.Photo
        fields = (
            "url",
            "id",
            "image",
            "galleries",
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
