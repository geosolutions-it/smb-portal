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
from django.db.models.signals import post_save


class ProfilesConfig(AppConfig):
    name = "profiles"

    def ready(self):
        from . import signals
        post_save.connect(
            signals.notify_profile_created,
            dispatch_uid=str(uuid.uuid4())
        )
