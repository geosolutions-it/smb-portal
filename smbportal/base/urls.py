#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""smbportal URL Configuration"""

from django.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("openid/", include("djangooidc.urls")),
    path(
        route="admin/",
        view=admin.site.urls
    ),
    path(
        route="",
        view=views.index,
        name="index"
    ),
    path(
        route="profile/",
        view=include("profiles.urls"),
        name="profile"
    ),
    path(
        route="bikes/",
        view=include("vehicles.urls"),
        name="bikes"
    ),
    path(
        route="observations/",
        view=include("vehiclemonitor.urls"),
        name="observations"
    ),
    path(
        route="openid/openid/KeyCloak",
        view=auth_views.login,
        name="login"
        ),
    path(
        route="avatar/",
        view=include("avatar.urls"),
        name="avatar",
    ),
    path(
        route="photologue/",
        view=include("photologue.urls", namespace="photologue")
    ),
    path(
        route="api/",
        view=include("api.urls"),
        name="api",
    ),
    path(
        route="api-auth/",
        view=include("rest_framework.urls", namespace="rest_framework"),
        name="api-auth",
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
