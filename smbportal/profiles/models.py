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
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.fields.files import ImageField


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
    user_avatar = ImageField(upload_to="MEDIA.ROOT.ASSETS", blank=True, null=True)

    @property
    def profile(self):
        attibute_names = (
            "enduserprofile",
            "prizemanagerprofile"
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
        blank=True,
        choices=(
            (FEMALE_GENDER, FEMALE_GENDER),
            (MALE_GENDER, MALE_GENDER),
        ),
    )
    phone_number = models.IntegerField(blank=True, null=True)
    bio = models.TextField(
        help_text="Short user biography",
        blank=True
    )
    


class Organization(models.Model):
    primary_key = models.AutoField(
        primary_key=True
        )
    organization_name = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        )
    role_in_organization = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        )
    type_of_interest_of_actor = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        )


class  PrizeManagerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank = True
    )
    
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        
    )
    language_preference = models.CharField(
        max_length=20,
        choices=((k, v) for k, v in settings.LANGUAGES),
        default="en"
    )
    acceptance_of_policy = models.BooleanField(
        default=False,
        
     )
    
class AnalystProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank = True
    )
    
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        
    )
    language_preference = models.CharField(
        max_length=20,
        choices=((k, v) for k, v in settings.LANGUAGES),
        default="en"
    )
    acceptance_of_policy = models.BooleanField(
        default=False,
        
     )
    
    
class AnalystSurvey(models.Model):
    HISTORIC = "Historical"
    REAL_TIME = "Real-time"
    SINGLE = "Single"
    AGGREGATED = "Aggregated"
    
    PDF = "pdf"
    SPATIAL = "Spatial"
    GRID_VECTOR = "Vector or Grid"
    objective_analysis = models.CharField(
        max_length=20,
        blank=False,
        null = False
        )
    common_interest = models.CharField(
        max_length=20,
        blank=True,
        null=True
        )    
    time_reference = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        choices = (
            (HISTORIC, "Historical data"),
            (REAL_TIME, "Real-time data"),
            )
        )
    analysis_numerosity = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices = (
            (SINGLE, "Single User"),
            (AGGREGATED, "Aggregated data" )
            
            )
        )
    graphs_of_interest = models.CharField(
        max_length=20,
        blank=True,
        null=True
        )
    
    of_interest_maps = models.CharField(
        max_length=20,
        blank=True,
        null=True
        )
    expected_output = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices = (
            (PDF,"a pdf file report"),
            (SPATIAL,"spatial analysis mapping"),
            (GRID_VECTOR,"files for export maps in grid or vector format")
            )
        )
class PrizeManagerSurvey(models.Model):
    BIKES = "Bikes"
    ON_FOOT = "By Foot"
    CAR_SHARING = "Car Sharing"
    PUBLIC_BIKE_SHARING = "Public Bike sharing"
    ELECTRIC_CAR_SHARING = "Electric Car sharing"
    
    FREE_TICKET = "free ticket"
    GIFT_ITEMS = "gift items"
    BOOK_DISCOUNT_COUPONS = "book of discount coupons of tickets"
    DISCOUNT_ON_PURCHASE = "discount on purchase subscription one-off"
    
    commercial_area_of_interest = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        )
    #
    reward_mode = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        choices = (
                (BIKES,' On Bikes'),
                (ON_FOOT,'By Foot'),
                (CAR_SHARING,'By Car Sharing'),
                (PUBLIC_BIKE_SHARING,'By Public Bike sharing'),
                (ELECTRIC_CAR_SHARING,'Electric Car sharing')
                )
        )
    type_of_offer = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        choices = (
            (FREE_TICKET,"free ticket"),
            (GIFT_ITEMS,"gift items"),
            (BOOK_DISCOUNT_COUPONS,"book of discount coupons of tickets"),
            (DISCOUNT_ON_PURCHASE,"discount on purchase subscription one-off"),
            )
        )
    reference_site = models.URLField(
        blank=True,
        null=True
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
