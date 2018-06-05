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

app_name = "bikes"
urlpatterns = [
    path(
        route="",
        view=views.BikeListView.as_view(),
        name="list"
    ),
    path(
        route="create",
        view=views.BikeCreateView.as_view(),
        name="create"
    ),
    path(
        route="<pk>",
        view=views.BikeDetailView.as_view(),
        name="detail"
    ),
    path(
        route="<pk>/update",
        view=views.BikeUpdateView.as_view(),
        name="update"
    ),
    path(
        route="<pk>/delete",
        view=views.BikeDeleteView.as_view(),
        name="delete"
    ),
    path(
        route="<pk>/pictures/upload",
        view=views.BikePictureUploadView.as_view(),
        name="picture-upload"
    ),
]
