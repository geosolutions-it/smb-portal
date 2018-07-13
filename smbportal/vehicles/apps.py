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

from django.apps import AppConfig
from django.db.models.signals import post_delete
from django.db.models.signals import post_save


class VehiclesConfig(AppConfig):
    name = "vehicles"

    def ready(self):
        from . import signals
        from . import models
        post_save.connect(
            signals.notify_bike_created,
            sender=models.Bike,
            dispatch_uid=str(uuid.uuid4())
        )
        post_delete.connect(
            signals.notify_bike_deleted,
            sender=models.Bike,
            dispatch_uid=str(uuid.uuid4())
        )
