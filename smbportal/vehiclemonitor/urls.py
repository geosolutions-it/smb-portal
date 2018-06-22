#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.urls import path

from . import views

app_name = "monitor"
urlpatterns = [
    path(
        route="<bike_pk>",
        view=views.BikeObservationListView.as_view(),
        name="list"
    ),
    # path(
    #     route="<bike_pk>/<pk>",
    #     view=views.BikeObservationDetailView.as_view(),
    #     name="detail"
    # ),
]
