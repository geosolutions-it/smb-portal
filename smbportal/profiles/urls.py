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

app_name = "profile"
urlpatterns = [
    path(
        route="",
        view=views.ProfileUpdateView.as_view(),
        name="update"
    ),
    path(
        route="create",
        view=views.EndUserProfileCreateView.as_view(),
        name="create"
    ),
    path(
        route="create-privileged",
        view=views.PrivilegedUserProfileCreateView.as_view(),
        name="create-privileged"
    ),
    path(
        route="surveys/create",
        view=views.MobilityHabitsSurveyCreateView.as_view(),
        name='create-survey'
    ),
    path(
        route="surveys/<pk>",
        view=views.MobilityHabitsSurveyDetailView.as_view(),
        name='survey'
    ),
]
