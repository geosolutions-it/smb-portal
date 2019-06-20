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

from django.template import Context
from django.template import Engine
from rest_framework import serializers

from .. import models

logger = logging.getLogger(__name__)


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sponsor
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
            {criterium: score for criterium, score in criteria.items()})
        return result


class PrizeSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer()

    class Meta:
        model = models.Prize
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
            winner = obj.competition.winners.get(user=self.context.get("user"))
        except models.Winner.DoesNotExist:
            result = string_template
        else:
            score = obj.competition.get_user_score(self.context["user"])
            formatted_score = ", ".join(
                "{}: {:0.3f}".format(criterium.value, value) for
                criterium, value in score.items()
            )
            context = Context({
                "rank": winner.rank,
                "score": formatted_score,
            })
            if "humanize" not in string_template:
                string_template = "{% load humanize %}" + string_template
            template = engine.from_string(string_template)
            result = template.render(context)
        return result

    class Meta:
        model = models.CompetitionPrize
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
        model = models.Competition
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
    sponsors = SponsorSerializer(many=True)

    def get_leaderboard(self, obj):
        board = obj.get_leaderboard()
        serializer = CompetitionRankingSerializer(instance=board, many=True)
        return serializer.data

    class Meta:
        model = models.Competition
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
            "sponsors",
        )


class UserCompetitionDetailSerializer(CompetitionDetailSerializer):
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        score = obj.get_user_score(self.context["user"])
        return {criterium.value: value for criterium, value in  score.items()}

    class Meta:
        model = models.CurrentCompetition
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

    def get_score(self, obj):
        score = obj.get_user_score(self.context["user"])
        return {criterium.value: value for criterium, value in  score.items()}


    class Meta:
        model = models.CurrentCompetition
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
