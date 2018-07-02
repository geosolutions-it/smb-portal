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
from django.contrib.auth.signals import user_logged_in


class BaseConfig(AppConfig):
    name = "base"

    def ready(self):
        from . import signals
        user_logged_in.connect(
            signals.set_user_language,
            dispatch_uid=str(uuid.uuid4())
        )
