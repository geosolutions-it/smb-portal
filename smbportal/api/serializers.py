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

import photologue.models
from rest_framework import serializers

import profiles.models
import vehicles.models


class SmbUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:users-detail",
    )

    class Meta:
        model = profiles.models.SmbUser
        fields = (
            "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "sub",
        )


class BikeListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bikes-detail",
    )
    owner = serializers.HyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:tags-detail",
        many=True,
        read_only=True
    )
    current_state = serializers.SerializerMethodField()

    def get_current_state(self, obj):
        return "yo"

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "nickname",
            "owner",
            "tags",
            "current_state",
            "last_update",
        )


class BikeDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bikes-detail",
    )
    owner = serializers.HyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:tags-detail",
        many=True,
        read_only=True
    )
    possession_history = serializers.HyperlinkedRelatedField(
        view_name="api:bike-possession-history-detail",
        many=True,
        read_only=True
    )
    picture_gallery = serializers.HyperlinkedRelatedField(
        view_name="api:picture-galleries-detail",
        read_only=True
    )

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "owner",
            "picture_gallery",
            "tags",
            "possession_history",
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
            "has_smb_sticker",
            "other_details",
        )


class PhysicalTagSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:tags-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        queryset=vehicles.models.Bike.objects.all(),
    )

    class Meta:
        model = vehicles.models.PhysicalTag
        fields = (
            "url",
            "bike",
            "epc",
        )


class BikePossessionHistorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bike-possession-history-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        read_only=True
    )
    reporter = serializers.HyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )

    class Meta:
        model = vehicles.models.BikePossessionHistory
        fields = (
            "url",
            "bike",
            "reporter",
            "possession_state",
            "creation_date",
            "details",
        )


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:picture-galleries-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
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
            "image",
            "galleries",
        )
