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
from itertools import product

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
import pytz

from profiles.models import EndUserProfile


class Prize(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("name"),
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True
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
    competition_definition = models.ForeignKey(
        "CompetitionDefinition",
        on_delete=models.CASCADE,
        verbose_name=_("competition definition")
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
            "competition_definition",
            "user_rank",
        )

    def __str__(self):
        return "{} - {} - (rank {})".format(
            self.competition_definition, self.prize, self.user_rank)


class CompetitionDefinition(models.Model):
    """Stores the definition for a competition"""
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
    REPEAT_WEEKLY = "repeat weekly"
    REPEAT_MONTHLY = "repeat monthly"
    REPEAT_YEARLY = "repeat yearly"
    REPEAT_IMMEDIATELY = "repeat immediately"

    name = models.CharField(
        verbose_name=_("name"),
        max_length=100
    )
    num_days = models.IntegerField(
        verbose_name=_("number of days"),
        default=7,
        help_text=_("Total number of days that this competition will run"),

    )
    starts_at = models.DateTimeField(
        verbose_name=_("starts at"),
    )
    num_repeats = models.IntegerField(
        verbose_name=_("number of repetitions"),
        default=0,
        help_text=_(
            "If this competition should be repeated or run only once. If set "
            "to 0 (the default), the competition will run only once. "
            "Otherwise, it will run for the specified number of times"
        )
    )
    repeat_when = models.CharField(
        max_length=50,
        verbose_name=_("repeat when"),
        choices=[
            (REPEAT_WEEKLY, _("repeat each week")),
            (REPEAT_MONTHLY, _("repeat each month")),
            (REPEAT_YEARLY, _("repeat each year")),
            (REPEAT_IMMEDIATELY, _("repeat immediately")),
        ],
        default=REPEAT_IMMEDIATELY,
        help_text=_(
            "If this competition is to be repeated, when should the next run "
            "start. If `immediately`, the new run will start on the next day "
            "after the previous one ends. If  one of the other options is "
            "selected, the next run will start on the same day as the "
            "previous, in the new temporal interval."
        )
    )
    age_group = ArrayField(
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
    segment_by_age_group = models.BooleanField(
        verbose_name=_("segment by age group"),
        default=True,
        help_text=_(
            "Whether this promotion is to be applied to each chosen age group "
            "separately or if the chosen age groups are to be merged into a "
            "single group. In the first case, there will be winners for each "
            "age group, while in the second case the winners will be elected "
            "from a pool of all users in the chosen age groups."
        )
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

    class Meta:
        ordering = (
            "name",
            "starts_at",
        )

    def __str__(self):
        return "{}".format(self.name)


class CurrentCompetitionManager(models.Manager):

    def get_queryset(self):
        now = dt.datetime.now(pytz.utc)
        return super().get_queryset().filter(
            start_date__lte=now, end_date__gte=now)


class CompetitionCreatorManager(models.Manager):

    def create_competitions(self, competition_definition):
        dates = get_competition_dates(
            competition_definition.num_repeats,
            competition_definition.starts_at,
            competition_definition.repeat_when,
            competition_definition.num_days
        )
        if competition_definition.segment_by_age_group:
            age_groups = competition_definition.age_group
        else:
            age_groups = [Competition.COMPOUND_AGE_GROUP]

        for date_pair, age_group in product(dates, age_groups):
            obj = self.model(
                competition_definition=competition_definition,
                age_group=age_group,
                start_date=date_pair[0],
                end_date=date_pair[1]
            )
            obj.save()



class Competition(models.Model):
    """Stores the result of a competition"""
    COMPOUND_AGE_GROUP = "compound_age_group"

    competition_definition = models.ForeignKey(
        "CompetitionDefinition",
        on_delete=models.CASCADE,
        verbose_name=_("competition definition")
    )
    age_group = models.CharField(
        max_length=50,
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
            (
                COMPOUND_AGE_GROUP,
                _("compound age group")
            ),
        ],
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

    objects = models.Manager()
    current_competitions_manager = CurrentCompetitionManager()
    creation_manager = CompetitionCreatorManager()

    class Meta:
        ordering = (
            "competition_definition",
            "age_group",
        )

    def __str__(self):
        return "Competition {!r} ({} - {})".format(
            self.competition_definition.name,
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d")
        )

    def is_open(self):
        now = dt.datetime.now(pytz.utc)
        return (now > self.start_date) and (now <= self.end_date)

    def get_leaderboard(self):
        pass


class CurrentCompetition(Competition):

    objects = CurrentCompetitionManager()

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


def get_competition_dates(num_repeats: int, start_date: dt.datetime,
                          repeat_frequency: str, duration_days: int):
    handler = {
        CompetitionDefinition.REPEAT_IMMEDIATELY: (
            get_competition_start_dates_immediate_frequency),
        CompetitionDefinition.REPEAT_WEEKLY: (
            get_competition_start_dates_weekly_frequency),
        CompetitionDefinition.REPEAT_MONTHLY: (
            get_competition_start_dates_monthly_frequency),
        CompetitionDefinition.REPEAT_YEARLY: (
            get_competition_start_dates_yearly_frequency),
    }.get(repeat_frequency)
    start_dates = handler(num_repeats, start_date, duration_days)
    return [(i, i + dt.timedelta(duration_days)) for i in start_dates]


def get_competition_start_dates_immediate_frequency(num_repeats: int,
                                                    start_date: dt.datetime,
                                                    duration_days: int):
    result = [start_date]
    for run in range(num_repeats):
        result.append(start_date + dt.timedelta(days=(duration_days+1) * run))
    return result


def get_competition_start_dates_weekly_frequency(num_repeats: int,
                                                 start_date: dt.datetime,
                                                 *args):
    result = [start_date]
    for run in range(num_repeats):
        result.append(start_date + dt.timedelta(days=7*run))
    return result


def get_competition_start_dates_monthly_frequency(num_repeats: int,
                                                  start_date: dt.datetime,
                                                  *args):
    days_in_previous_month = calendar.monthrange(
        start_date.year, start_date.month)[1]
    nth_start_date = start_date
    result = [start_date]
    for run in range(num_repeats):
        nth_start_date = nth_start_date + dt.timedelta(
            days=days_in_previous_month)
        days_in_previous_month = calendar.monthrange(
            nth_start_date.year, nth_start_date.month)[1]
        result.append(nth_start_date)
    return result


def get_competition_start_dates_yearly_frequency(num_repeats: int,
                                                 start_date: dt.datetime,
                                                 *args):
    days_in_previous_year = 366 if calendar.isleap(start_date.year) else 365
    nth_start_date = start_date
    result = [start_date]
    for run in range(num_repeats):
        nth_start_date = nth_start_date + dt.timedelta(
            days=days_in_previous_year)
        result.append(nth_start_date)
        days_in_previous_year = (
            366 if calendar.isleap(nth_start_date.year) else 365)
    return result
