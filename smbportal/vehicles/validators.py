#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Validators for forms and models"""

import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def validate_file_size(value):
    max_size_mega_bytes = settings.SMB_PORTAL.get(
        "max_upload_size_megabytes", 3)
    max_size = max_size_mega_bytes * 1024**2
    logger.debug("value.size: {}".format(value.size))
    logger.debug("max_size: {}".format(max_size))
    if value.size > max_size:
        logger.debug("about to raise ValidationError...")
        raise ValidationError(
            _("Uploaded file is too large. File size must not exceed "
              "%(max_size)s MB"),
            params={"max_size": max_size_mega_bytes},
            code="invalid"
        )
