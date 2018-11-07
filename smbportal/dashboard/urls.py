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

app_name = "dashboard"
urlpatterns = [
    path(
        route="",
        view=views.dashboard_downloads,
        name="index"
    ),
    # path(
    #     route="download-segments",
    #     view=views.download_segments,
    #     name="download-segments"
    # ),
    # path(
    #     route="download-observations",
    #     view=views.download_observations,
    #     name="download-observations"
    # ),
]
