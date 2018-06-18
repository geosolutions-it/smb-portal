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

import profiles.models
import vehicles.models

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
                "pk": obj.keycloak.UID
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
                "pk": obj.keycloak.UID
            },
            request=request,
            format=format
        )

    def get_object(self, view_name, view_args, view_kwargs):
        return self.get_queryset().get(kycloak__UID=view_kwargs.get("pk"))

    def use_pk_only_optimization(self):
        return False


class SmbUserSerializer(serializers.HyperlinkedModelSerializer):
    url = SmbUserHyperlinkedIdentityField(
        view_name="api:users-detail",
    )
    id = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    profile_type = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.keycloak.UID

    def get_profile(self, obj):
        if obj.profile is not None:
            profile_class = type(obj.profile)
            serializer_class = {
                profiles.models.EndUserProfile: EndUserProfileSerializer,
                profiles.models.PrivilegedUserProfile: (
                    PrivilegedUserProfileSerializer),
            }.get(profile_class)
            logger.debug("serializer_class: {}".format(serializer_class))
            serializer = serializer_class(
                instance=obj.profile,
                context=self.context
            )
            logger.debug("serializer: {}".format(serializer))
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
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
            "profile",
            "profile_type",
        )


class EndUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = profiles.models.EndUserProfile
        fields = (
            "gender",
            "phone_number",
            "bio",
            "date_updated",
        )


class PrivilegedUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = profiles.models.PrivilegedUserProfile
        fields = ()


class BikeListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bikes-detail",
    )
    owner = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:tags-detail",
        many=True,
        read_only=True
    )
    current_status = serializers.SerializerMethodField()

    def get_current_status(self, obj):
        current_status = obj.get_current_status()
        url = reverse(
            viewname="api:statuses-detail",
            kwargs={"pk": current_status.pk}
        )
        return url

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "nickname",
            "owner",
            "tags",
            "current_status",
            "last_update",
        )


class BikeDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:bikes-detail",
    )
    owner = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )
    tags = serializers.HyperlinkedRelatedField(
        view_name="api:tags-detail",
        many=True,
        read_only=True
    )
    status_history = serializers.HyperlinkedRelatedField(
        view_name="api:statuses-detail",
        many=True,
        read_only=True
    )
    picture_gallery = serializers.HyperlinkedRelatedField(
        view_name="api:picture-galleries-detail",
        read_only=True
    )
    current_status = serializers.SerializerMethodField()

    def get_current_status(self, obj):
        current_status = obj.get_current_status()
        serializer = BikeStatusSerializer(
            instance=current_status,
            context=self.context
        )
        return serializer.data

    class Meta:
        model = vehicles.models.Bike
        fields = (
            "url",
            "owner",
            "picture_gallery",
            "tags",
            "status_history",
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
            "current_status",
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
            "creation_date",
        )


class MyBikeStatusSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:statuses-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        queryset=vehicles.models.Bike.objects.all()
    )
    reporter = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        read_only=True
    )

    class Meta:
        model = vehicles.models.BikeStatus
        fields = (
            "url",
            "bike",
            "reporter",
            "lost",
            "creation_date",
            "details",
        )

    def save(self, **kwargs):
        request = self.context.get("request")
        current_user = request.user
        return super().save(
            reporter=current_user
        )


class BikeStatusSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:statuses-detail",
    )
    bike = serializers.HyperlinkedRelatedField(
        view_name="api:bikes-detail",
        queryset=vehicles.models.Bike.objects.all()
    )
    reporter = SmbUserHyperlinkedRelatedField(
        view_name="api:users-detail",
        queryset=profiles.models.SmbUser.objects.all()
    )

    class Meta:
        model = vehicles.models.BikeStatus
        fields = (
            "url",
            "bike",
            "reporter",
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
