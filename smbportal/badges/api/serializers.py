#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""API serializers for badges"""

import logging

import django_gamification.models as gm
from rest_framework.reverse import reverse
from rest_framework import serializers

logger = logging.getLogger(__name__)


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

