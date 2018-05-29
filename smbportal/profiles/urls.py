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
    path("", views.EndUserProfileDetailView.as_view(), name="detail"),
    #only here until i can figure out why it wont work above
    path("details",views.EndUserProfileUpdateDetailView.as_view(), name="details"),
    path("create", views.EndUserProfileCreateView.as_view(), name="create"),
    path("update", views.EndUserProfileUpdateView.as_view(), name="update"),
    path("create/survey",views.EndUserSurvey.as_view(),name='createsurvey'),
]
