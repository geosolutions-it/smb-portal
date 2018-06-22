#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################
from vehicles import models


def get_current_bike(view_kwargs, pk_attr_name="pk"):
    try:
        bike = models.Bike.objects.get(pk=view_kwargs.get(pk_attr_name))
    except models.Bike.DoesNotExist:
        bike = None
    return bike