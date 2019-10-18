#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Serializers for the smbportal REST API

These serializers deal with 3rd party packages, like ``photologue``

"""

import logging

import photologue.models
from rest_framework import serializers

logger = logging.getLogger(__name__)


class PictureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = photologue.models.Photo
        fields = (
            "id",
            "image",
        )
