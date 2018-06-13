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
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone


class BikeObservation(gis_models.Model):
    bike = models.ForeignKey(
        "vehicles.Bike",
        on_delete=models.CASCADE,
        related_name="observations",
    )
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    position = gis_models.PointField(
        null=True,
        blank=True,
        help_text="Either this field or `address` must be given"
    )
    address = models.CharField(
        max_length=255,
        help_text="Approximate address. Either this field or `position` must "
                  "be given",
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    observed_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the observation was made."
    )
    details = models.TextField(blank=True)

    class Meta:
        ordering = (
            "-observed_at",
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        has_address = bool(self.address)
        has_position = bool(self.position)
        if not has_address and not has_position:
            raise RuntimeError("Specify one of `position` or `address`")
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)
