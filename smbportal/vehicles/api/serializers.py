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

from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

import vehicles.models

from api.serializers import PictureSerializer
from profiles.api.fields import SmbUserHyperlinkedRelatedField

logger = logging.getLogger(__name__)


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
