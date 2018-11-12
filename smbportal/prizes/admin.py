#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib import admin

from . import models


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
    )
    list_filter = (
        "age_groups",
        "start_date",
    )


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
        "competition",
        "user",
        "rank",
    )
