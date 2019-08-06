#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import ugettext_lazy as _

from . import models
from . import utils


@admin.register(models.Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "age_groups",
        "criteria",
        "is_open",
        "show_regions",
    )
    list_filter = (
        "age_groups",
        "start_date",
        "regions",
    )
    filter_horizontal = (
        "regions",
    )

    def show_regions(self, obj):
        return list(obj.regions.values_list("name", flat=True))
    show_regions.short_description = "regions"


@admin.register(models.CurrentCompetition)
class CurrentCompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "age_groups",
    )
    list_filter = (
        "age_groups",
        "start_date",
    )

    def get_queryset(self, request):
        return self.model.objects.get_queryset()


@admin.register(models.FinishedCompetition)
class FinishedCompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "end_date",
        "age_groups",
    )
    list_filter = (
        "age_groups",
        "start_date",
    )

    def get_queryset(self, request):
        return self.model.objects.get_queryset()


@admin.register(models.CompetitionPrize)
class CompetitionPrizeAdmin(admin.ModelAdmin):
    list_display = (
        "prize",
        "competition",
        "user_rank",
        "prize_attribution_template"
    )
    list_filter = (
        "prize",
        "competition",
    )


@admin.register(models.Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "participant_user",
        "participant_competition",
        "rank",
    )

    def participant_user(self, winner: models.Winner):
        return winner.participant.user

    participant_user.short_description = _("user")
    participant_user.admin_order_field = "participant__user"

    def participant_competition(self, winner: models.Winner):
        return winner.participant.competition

    participant_competition.short_description = _("competitition")
    participant_competition.admin_order_field = "participant__competition"


def approve_participant(model_admin, request, queryset):
    _moderate_participant(
        model_admin, models.CompetitionParticipant.APPROVED,request, queryset)
approve_participant.short_description = _("Approve participants")


def reject_participant(model_admin, request, queryset):
    _moderate_participant(
        model_admin, models.CompetitionParticipant.REJECTED,request, queryset)
reject_participant.short_description = _("Reject participants")


def _moderate_participant(model_admin, status, request, queryset):
    rows_updated = utils.moderate_competition_participation_request(
        queryset,
        status,
        request
    )
    model_admin.message_user(
        request,
        _(f"{rows_updated} participation requests have been {status}")
    )


@admin.register(models.CompetitionParticipant)
class CompetitionParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "competition",
        "user",
        "registration_status",
    )
    actions = [
        approve_participant,
        reject_participant,
    ]
    list_filter = (
        "registration_status",
    )


@admin.register(models.PendingCompetitionParticipant)
class PendingCompetitionParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "competition",
        "user",
    )
    actions = [
        approve_participant,
        reject_participant,
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(models.RegionOfInterest)
class RegionOfInterestAdmin(OSMGeoAdmin):
    map_width = 900
    map_height = 600

    list_display = (
        "id",
        "name",
    )
