#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from base.utils import get_current_bike
from . import models

logger = logging.getLogger(__name__)


class BikeObservationListView(LoginRequiredMixin, PermissionRequiredMixin,
                              ListView):
    context_object_name = "observations"
    permission_required = "vehiclemonitor.can_list_own_bike_observation"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["bike"] = get_current_bike(self.kwargs, "bike_pk")
        return context_data

    def get_queryset(self):
        current_bike = get_current_bike(self.kwargs, "bike_pk")
        qs = models.BikeObservation.objects.filter(
            bike__owner=self.request.user)
        if current_bike is not None:
            qs = qs.filter(bike=current_bike)
        num_observations = settings.SMB_PORTAL.get("num_latest_observations")
        return qs.order_by("-observed_at")[:num_observations]
