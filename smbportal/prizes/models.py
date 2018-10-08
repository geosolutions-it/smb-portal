#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import datetime as dt
import calendar

from django.db import connections
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from smbbackend import calculateprizes
import pytz

from profiles.models import EndUserProfile


class Sponsor(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("sponsor")
    )
    logo = models.ImageField(
        verbose_name="logo",
        null=True,
        blank=True,
    )
    url = models.URLField(
        verbose_name=_("url"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Prize(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("name"),
    )
    image = models.ImageField(
        verbose_name="image",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True
    )
    sponsor = models.ForeignKey(
        "Sponsor",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("sponsor"),
    )
    url = models.URLField(
        verbose_name=("url"),
        null=True,
        blank=True,
        help_text=_(
            "URL where more information about this prize can be obtained")
    )

    class Meta:
        ordering = (
            "name",
        )

    def __str__(self):
        return self.name


class CompetitionPrize(models.Model):
    prize = models.ForeignKey(
        "Prize",
        on_delete=models.CASCADE,
        verbose_name=_("prize"),
    )
    competition = models.ForeignKey(
        "Competition",
        on_delete=models.CASCADE,
        verbose_name=_("competition")
    )
    user_rank = models.IntegerField(
        verbose_name=_("user rank"),
        null=True,
        blank=True,
        help_text=_(
            "Rank that the user must attain in the underlying competition in "
            "order to be awarded the prize. If None, all of the competition'"
            "s winners will be awarded the prize"
        )
    )

    class Meta:
        ordering = (
            "prize",
            "competition",
            "user_rank",
        )

    def __str__(self):
        return "{} - {} - (rank {})".format(
            self.competition, self.prize, self.user_rank)


class CurrentCompetitionManager(models.Manager):

    def get_queryset(self):
        now = dt.datetime.now(pytz.utc)
        return super().get_queryset().filter(
            start_date__lte=now, end_date__gte=now)


class FinishedCompetitionManager(models.Manager):

    def get_queryset(self):
        now = dt.datetime.now(pytz.utc)
        return super().get_queryset().filter(end_date__lte=now)


class Competition(models.Model):
    """Stores the result of a competition"""

    CRITERIUM_SAVED_SO2_EMISSIONS = "saved SO2 emissions"
    CRITERIUM_SAVED_NOX_EMISSIONS = "saved NOx emissions"
    CRITERIUM_SAVED_CO2_EMISSIONS = "saved CO2 emissions"
    CRITERIUM_SAVED_CO_EMISSIONS = "saved CO emissions"
    CRITERIUM_SAVED_PM10_EMISSIONS = "saved PM10 emissions"
    CRITERIUM_CONSUMED_CALORIES = "consumed calories"
    CRITERIUM_BIKE_USAGE_FREQUENCY = "bike usage frequency"
    CRITERIUM_PUBLIC_TRANSPORT_USAGE_FREQUENCY = (
        "public transport usage frequency")
    CRITERIUM_BIKE_DISTANCE = "bike distance"
    CRITERIUM_SUSTAINABLE_MEANS_DISTANCE = "sustainable means distance"

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True
    )
    age_groups = ArrayField(
        base_field=models.CharField(
            max_length=10,
            choices=[
                (
                    EndUserProfile.AGE_YOUNGER_THAN_NINETEEN,
                    _("< 19")
                ),
                (
                    EndUserProfile.AGE_BETWEEN_NINETEEN_AND_THIRTY,
                    _("19 - 30")
                ),
                (
                    EndUserProfile.AGE_BETWEEN_THIRTY_AND_SIXTY_FIVE,
                    _("30 - 65")
                ),
                (
                    EndUserProfile.AGE_OLDER_THAN_SIXTY_FIVE,
                    _("65+")
                ),
            ]
        ),
        size=4,
        verbose_name=_("age group"),
    )
    start_date = models.DateTimeField(
        verbose_name=_("start date"),
        help_text=_("Date when the competition started"),
        editable=False,
    )
    end_date = models.DateTimeField(
        verbose_name=_("end date"),
        help_text=_("Date when the competition ended"),
        editable=False,
    )
    criteria = ArrayField(
        base_field=models.CharField(
            max_length=100,
            choices=[
                (CRITERIUM_SAVED_CO2_EMISSIONS, _("saved CO2 emissions")),
                (CRITERIUM_SAVED_NOX_EMISSIONS, _("saved NOx emissions")),
                (CRITERIUM_SAVED_CO2_EMISSIONS, _("saved CO2 emissions")),
                (CRITERIUM_SAVED_CO_EMISSIONS, _("saved CO emissions")),
                (CRITERIUM_SAVED_PM10_EMISSIONS, _("saved PM10 emissions")),
                (CRITERIUM_CONSUMED_CALORIES, _("consumed calories")),
                (CRITERIUM_BIKE_USAGE_FREQUENCY, _("bike usage frequency")),
                (
                    CRITERIUM_PUBLIC_TRANSPORT_USAGE_FREQUENCY,
                    _("public transport usage frequency")
                ),
                (CRITERIUM_BIKE_DISTANCE, _("bike distance")),
                (
                    CRITERIUM_SUSTAINABLE_MEANS_DISTANCE,
                    _("sustainable means distance")
                ),
            ]
        ),
        verbose_name=_("criteria"),
        help_text=_(
            "Which criteria will be used for deciding who wins the "
            "competition"
        )
    )
    winner_threshold = models.IntegerField(
        verbose_name=_("winner threshold"),
        default=1,
        help_text=_(
            "After results are calculated and ordered, how many of the top "
            "users should be considered winners? The winners will earn the "
            "prizes specified in this competition."
        )
    )

    objects = models.Manager()
    current_competitions_manager = CurrentCompetitionManager()

    class Meta:
        ordering = (
            "name",
            "start_date",
            "end_date",
            "age_groups",
        )

    def __str__(self):
        return "Competition {!r} ({} - {})".format(
            self.name,
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d")
        )

    def is_open(self):
        now = dt.datetime.now(pytz.utc)
        return (now > self.start_date) and (now <= self.end_date)

    def get_leaderboard(self):
        leaderboard = calculateprizes.get_leaderboard(
            self._as_competition_info(),
            connections["default"].connection.cursor()
        )
        user_model = get_user_model()
        result = []
        for entry in leaderboard:
            user = user_model.objects.get(id=entry["user"])
            result.append((user, entry["criteria_points"]))
        return result

    def get_user_score(self, user):
        return calculateprizes.get_user_score(
            self._as_competition_info(),
            user.pk,
            connections["default"].connection.cursor()
        )

    def _as_competition_info(self):
        return calculateprizes.CompetitionInfo(
            id=self.id,
            name=self.name,
            criteria=self.criteria,
            winner_threshold=self.winner_threshold,
            start_date=self.start_date,
            end_date=self.end_date,
            age_groups=self.age_groups,
        )


class CurrentCompetition(Competition):

    objects = CurrentCompetitionManager()

    class Meta:
        proxy = True


class FinishedCompetition(Competition):

    objects = FinishedCompetitionManager()

    class Meta:
        proxy = True


class Winner(models.Model):
    """Stores the winners of competitions"""
    competition = models.ForeignKey(
        "Competition",
        verbose_name=_("competition"),
        on_delete=models.CASCADE,
        related_name="winners",
    )
    user = models.ForeignKey(
        "profiles.SmbUser",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="competitions_won"
    )
    rank = models.IntegerField(
        verbose_name=_("rank"),
    )

    class Meta:
        ordering = (
            "competition",
            "rank",
            "user",
        )

    def __str__(self):
        return "Competition {!r} ({} - {})".format(
            self.competition,
            self.user,
            self.rank
        )
