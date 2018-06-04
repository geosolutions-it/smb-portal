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
        route=r"admin/",
        view=admin.site.urls
    ),
    path(
        route=r"",
        view=views.index,
        name="index"
    ),
    path(
        route=r"profile/",
        view=include("profiles.urls"),
        name="profile"
    ),
    path(
        route=r"bikes/",
        view=include("vehicles.urls"),
        name="bikes"
    ),
    path(
        route=r"openid/openid/KeyCloak",
        view= auth_views.login,
        name="login"
        ),
    
    path(
        route=r"avatar/",
        view=include("avatar.urls"),
        name="avatar",
    ),
    path(
        route=r"photologue/",
        view=include("photologue.urls", namespace="photologue")
    ),
    path(
        route=r"api/",
        view=include("api.urls"),
        name="api",
    ),
    path(
        route=r"api-auth/",
        view=include("rest_framework.urls", namespace="rest_framework"),
        name="api-auth",
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
