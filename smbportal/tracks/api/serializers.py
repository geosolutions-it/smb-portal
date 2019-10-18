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


from profiles.api.fields import SmbUserHyperlinkedRelatedField
from .. import models

logger = logging.getLogger(__name__)


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
        model = models.Track
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
            "is_valid",
            "validation_error",
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
        model = models.Track
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
            "is_valid",
            "validation_error",
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
        model = models.Track
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
            "is_valid",
            "validation_error",
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
        model = models.Track
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
            "is_valid",
            "validation_error",
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
        try:
            emissions = obj.emission
            serializer = EmissionSerializer(
                instance=emissions, context=self.context)
            result = serializer.data
        except models.Emission.DoesNotExist:
            result = None
        return result

    def get_costs(self, obj):
        try:
            costs = obj.cost
            serializer = CostSerializer(
                instance=costs, context=self.context)
            result = serializer.data
        except models.Cost.DoesNotExist:
            result = None
        return result

    def get_health(self, obj):
        try:
            health = obj.health
            serializer = HealthSerializer(
                instance=health, context=self.context)
            result = serializer.data
        except models.Health.DoesNotExist:
            result = None
        return result

    class Meta:
        model = models.Segment
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
        model = models.Segment
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
        model = models.Segment
        fields = (
            "id",
            "url",
            "geom"
        )


class MyBriefSegmentSerializer(MySegmentSerializer):
    class Meta:
        model = models.Segment
        fields = (
            "id",
            "url",
            "geom"
        )


class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Emission
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
        model = models.Cost
        fields = (
            "fuel_cost",
            "time_cost",
            "depreciation_cost",
            "operation_cost",
            "total_cost",
        )


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Health
        fields = (
            "calories_consumed",
            "benefit_index",
        )
