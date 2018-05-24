#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# TODO: Integrate with django-avatar for avatar support
# TODO: Decide on and improve integration with external tables
class SmbUser(AbstractUser):
    """Default user model for smb-portal.

    This model's schema cannot be changed at-will.
    This model has some unusual properties, like the custom ``db_table``
    meta option and the mapping of some attributes to explicit table_column
    names. This is due to the fact that the database table that is used by the
    model is being shared between the smb-portal and other smb apps.

    Some of the underlying DB table columns are not needed for the smb-portal
    and are therefore not mapped to any django model attributes.

    """

    nickname = models.CharField(
        max_length=100,
        db_column="preferred_username"
    )
    sub = models.TextField(
        help_text="The OpenID Direct subject. This is the effective user "
                  "identifier in the authentication provider",
        unique=True
    )
    language_preference = models.CharField(
        choices=((k, v) for k, v in settings.LANGUAGES.items()),
        default="en"
    )
    # ``cognito:user_status`` column is not mapped to this model
    # ``status`` column is not mapped to this model
    # ``_id`` column is not mapped to this model

    class Meta:
        db_table = "users"
        managed = False


# TODO: Integrate data sharing policies
class EndUserProfile(models.Model):
    MALE_GENDER = "male"
    FEMALE_GENDER = "female"

    PUBLIC = "public"
    COMMUNITY = "community"
    PRIVATE = "private"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    gender = models.CharField(
        choices=(
            (FEMALE_GENDER, FEMALE_GENDER),
            (MALE_GENDER, MALE_GENDER),
        ),
        max_length=20
    )
    phone_number = models.IntegerField(blank=True, null=True)
    bio = models.TextField(
        help_text="Short user biography"
    )


class MobilityHabitsSurvey(models.Model):
    FREQUENT_PUBLIC_TRANSPORT_USER = "frequent"
    OCCASIONAL_PUBLIC_TRANSPORT_USER = "occasional"
    RARE_PUBLIC_TRANSPORT_USER = "rare"
    NOT_A_PUBLIC_TRANSPORT_USER = "never"

    FREQUENT_BICYCLE_USER = "frequent"
    OCCASIONAL_BICYCLE_USER = "occasional"
    SEASONAL_BICYCLE_USER = "seasonal"
    RARE_BICYCLE_USER = "rare"
    NOT_A_BICYCLE_USER = "never"

    end_user = models.ForeignKey(
        "EndUserProfile",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    date_answered = models.DateTimeField(
        auto_now_add=True
    )
    public_transport_usage = models.CharField(
        max_length=100,
        choices=(
            (
                FREQUENT_PUBLIC_TRANSPORT_USER,
                "Habitual (more than 10 travels per month)"
            ),
            (
                OCCASIONAL_PUBLIC_TRANSPORT_USER,
                "Occasional (once per month)"
            ),
            (
                RARE_PUBLIC_TRANSPORT_USER,
                "Rare (less than 10 travels per year)"
            ),
            (
                NOT_A_PUBLIC_TRANSPORT_USER,
                "Never"
            ),
        )
    )
    uses_bike_sharing_services = models.BooleanField(
        default=False
    )
    uses_electrical_car_sharing_services = models.BooleanField(
        default=False
    )
    uses_fuel_car_sharing_services = models.BooleanField(
        default=False
    )
    bicycle_usage = models.CharField(
        max_length=100,
        choices=(
            (
                FREQUENT_BICYCLE_USER,
                "Habitual (at least once a week on average)"
            ),
            (
                OCCASIONAL_BICYCLE_USER,
                "Habitual (at least once a month)"
            ),
            (
                SEASONAL_BICYCLE_USER,
                "Seasonal (mainly used in the Summer)"
            ),
            (
                RARE_BICYCLE_USER,
                "Rare (less than once a month)"
            ),
            (
                NOT_A_BICYCLE_USER,
                "Never use a bicycle to move around in the city"
            ),
        )

    )
