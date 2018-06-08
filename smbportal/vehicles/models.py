#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import uuid

from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from photologue.models import Gallery


class Vehicle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    last_position = models.ForeignKey(
        "tracks.CollectedPoint",
        models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class BikeManager(models.Manager):

    def create(self, *args, **kwargs):
        """Create instances

        Automatically create a possession state and a gallery whenever a new
        bike is saved

        """

        bike = self.model(
            *args,
            **kwargs
        )
        bike.save()
        possession_history = BikePossessionHistory(
            bike=bike,
            reporter=bike.owner,
        )
        possession_history.save()
        gallery_title = "Picture gallery for bike {}".format(bike.pk)
        picture_gallery = Gallery.objects.create(
            title=gallery_title,
            slug=slugify(gallery_title),
        )
        bike.picture_gallery = picture_gallery
        bike.save()
        return bike


# TODO: Add custom managers for retrieving stolen bikes and lost bikes
# TODO: Integrate django-photolog for bike picture gallery
class Bike(Vehicle):
    RACING_BIKE = "racing"
    CITY_BIKE = "city"
    MOUNTAIN_BIKE = "mountain"
    FOLDABLE_BIKE = "foldable"

    SINGLE_RING_GEAR = "single ring"
    GROUPSET_UNDER_18_SPEED_GEAR = "groupset below 18 speeds"
    GROUPSET_ABOVE_18_SPEED_GEAR = "groupset above 18 speeds"
    ELECTRIC_GEAR = "electric"

    DISK_BRAKE = "disk"
    CANTILEVER_BRAKE = "cantilever"
    COASTER_BRAKE = "coaster"

    objects = BikeManager()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bikes",
    )
    picture_gallery = models.OneToOneField(
        "photologue.Gallery",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    last_update = models.DateTimeField(
        auto_now=True,
        db_column="lastupdate",
    )
    bike_type = models.CharField(
        max_length=20,
        choices=(
            (RACING_BIKE, RACING_BIKE),
            (CITY_BIKE, CITY_BIKE),
            (MOUNTAIN_BIKE, MOUNTAIN_BIKE),
            (FOLDABLE_BIKE, FOLDABLE_BIKE),
        ),
        default=CITY_BIKE,
    )
    gear = models.CharField(
        max_length=50,
        choices=(
            (SINGLE_RING_GEAR, SINGLE_RING_GEAR),
            (GROUPSET_UNDER_18_SPEED_GEAR, GROUPSET_UNDER_18_SPEED_GEAR),
            (GROUPSET_ABOVE_18_SPEED_GEAR, GROUPSET_ABOVE_18_SPEED_GEAR),
            (ELECTRIC_GEAR, ELECTRIC_GEAR),
        ),
        default=GROUPSET_ABOVE_18_SPEED_GEAR,
    )
    brake = models.CharField(
        max_length=30,
        choices=(
            (DISK_BRAKE, DISK_BRAKE),
            (CANTILEVER_BRAKE, CANTILEVER_BRAKE),
            (COASTER_BRAKE, COASTER_BRAKE),
        ),
        default=DISK_BRAKE,
    )
    nickname = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=100, blank=True)
    saddle = models.CharField(max_length=100, blank=True)
    has_basket = models.BooleanField(default=False)
    has_cargo_rack = models.BooleanField(default=False)
    has_lights = models.BooleanField(default=False)
    has_bags = models.BooleanField(default=False)
    has_smb_sticker = models.BooleanField(
        default=False,
        verbose_name="has SaveMyBike sticker"
    )
    other_details = models.TextField(blank=True)

    def __str__(self):
        return "{0.id}({0.nickname})".format(self)

    def get_absolute_url(self):
        return reverse("bikes:detail", kwargs={"pk": self.id})

    def get_current_possession_state(self):
        return self.possession_history.order_by("-creation_date").first()

    def report_possession_state(self, state, reporter=None, details=None):
        state_obj = BikePossessionHistory(
            bike=self,
            reporter=reporter if reporter is not None else self.owner,
            possession_state=state,
            details=details if details is not None else ""
        )
        state_obj.full_clean()
        state_obj.save()


class BikePossessionHistory(models.Model):
    WITH_OWNER = "with owner"
    LOST = "lost"
    STOLEN = "stolen"
    FOUND_BY_THIRD_PARTY = "found by third party"

    bike = models.ForeignKey(
        "Bike",
        on_delete=models.CASCADE,
        related_name="possession_history"
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    possession_state = models.CharField(
        max_length=50,
        choices=(
            (WITH_OWNER, WITH_OWNER),
            (LOST, LOST),
            (STOLEN, STOLEN),
            (FOUND_BY_THIRD_PARTY, FOUND_BY_THIRD_PARTY),
        ),
        default=WITH_OWNER,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(
        blank=True
    )

    def __str__(self):
        return "{0.possession_state}({0.creation_date})".format(self)

    class Meta:
        ordering = [
            "-creation_date",
        ]


class PhysicalTag(models.Model):
    bike = models.ForeignKey(
        "Bike",
        on_delete=models.CASCADE,
        related_name="tags",
    )
    epc = models.TextField(
        help_text="Electronic Product Code"
    )
    creation_date = models.DateTimeField(auto_now_add=True)
