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
from .. import utils

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

    def get_winner_description(
            self,
            obj: models.CompetitionPrize
    ):
        engine = Engine.get_default()
        string_template = obj.prize_attribution_template
        try:
            winner = models.Winner.objects.get(
                participant__user=self.context.get("user"),
                participant__competition=obj.competition
            )
        except models.Winner.DoesNotExist:
            result = string_template
        else:
            score = winner.participant.get_score()
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


class CompetitionParticipantDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:my-competitions-current-detail",
    )
    score = serializers.SerializerMethodField()
    competition = CompetitionDetailSerializer()

    def get_score(self, participant: models.CompetitionParticipant):
        status = participant.registration_status
        if status == models.CompetitionParticipant.APPROVED:
            score = participant.get_score()
            result = {
                criterium.value: value for criterium, value in  score.items()}
        else:
            result = None
        return result

    class Meta:
        model = models.CompetitionParticipant
        fields = (
            "id",
            "url",
            "registration_status",
            "score",
            "competition",
        )


class CompetitionParticipantRequestSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()

    def validate_competition_id(self, value):
        try:
            competition = models.Competition.objects.get(pk=value)
        except models.Competition.DoesNotExist:
            raise serializers.ValidationError("Invalid competition_id")
        else:
            already_exists = models.CompetitionParticipant.objects.filter(
                user=self.context["user"],
                competition=competition
            ).exists()
            if already_exists:
                raise serializers.ValidationError(
                    "User is already subscribed to the selected "
                    "competition"
                )
            else:
                available_competitions = utils.get_available_competitions(
                    self.context["user"])
                if competition not in available_competitions:
                    raise serializers.ValidationError(
                        "User cannot join the selected competition")
                else:
                    result = value
            return result

    def create(self, validated_data):
        competition = models.Competition.objects.get(
            pk=validated_data["competition_id"])
        user = self.context["user"]
        participant = utils.sign_up_for_competition(
            user,
            competition,
            request=self.context["request"],
            approved=False,
        )
        return participant
