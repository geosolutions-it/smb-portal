#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Development Django settings for smbportal"""

from .base import *

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "djangooidc": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "base": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "profiles": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "vehicles": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "vehiclemonitor": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "keycloakauth": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "api": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}
