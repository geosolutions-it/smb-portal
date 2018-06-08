#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


# TODO: Integrate with django-avatar for avatar support
# TODO: do we need to add the `status` attribute?
# TODO: do we need to add the `_id` attribute?
class SmbUser(AbstractUser):
    """Default user model for smb-portal.

    This model's schema cannot be changed at-will since the underlying DB table
    is shared with other smb apps

    """

    nickname = models.CharField(
        max_length=100,
    )
    language_preference = models.CharField(
        max_length=20,
        choices=((k, v) for k, v in settings.LANGUAGES),
        default="en"
    )
    sub = models.TextField(
        help_text="The OpenID Direct subject. This is the effective user "
                  "identifier in the authentication provider. This attribute "
                  "is required by other smb apps, it is not used "
                  "by smb-portal",
        blank=True
    )
    cognito_user_status = models.BooleanField(
        default=True,
        help_text="This attribute is required by other smb apps, it is not "
                  "used by smb-portal"
    )

    @property
    def profile(self):
        attibute_names = (
            "enduserprofile",
            "privilegeduserprofile",
            # add more profiles for analysts, prize managers, etc
        )
        for attr in attibute_names:
            try:
                profile = getattr(self, attr)
                break
            except AttributeError:
                pass
        else:
            profile = None
        return profile


# TODO: Integrate data sharing policies
class EndUserProfile(models.Model):
    MALE_GENDER = "male"
    FEMALE_GENDER = "female"

    PUBLIC = "public"
    COMMUNITY = "community"
    PRIVATE = "private"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    gender = models.CharField(
        max_length=20,
        blank=False,
        choices=(
            (FEMALE_GENDER, FEMALE_GENDER),
            (MALE_GENDER, MALE_GENDER),
        ),
        default=FEMALE_GENDER,
    )
    PHONE_NUMBER_REGEX_VALIDATOR = RegexValidator(
        r"^\+\d{8,15}$",
        message="Use the format +99999999. From 8 to 15 digits allowed"
    )
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        validators=[PHONE_NUMBER_REGEX_VALIDATOR]
    )
    bio = models.TextField(
        help_text="Short user biography",
        blank=True
    )

    def get_absolute_url(self):
        return reverse("profile:update")


class PrivilegedUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
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
        null=True,
        related_name="mobility_habits_surveys"
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

    def get_absolute_url(self):
        return reverse("profile:survey", kwargs={"pk": self.pk})
