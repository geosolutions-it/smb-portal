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
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        route="i18n/",
        view=include("django.conf.urls.i18n")
    ),
    path(
        route="admin/",
        view=admin.site.urls
    ),
    path(
        route="openid/",
        view=include("djangooidc.urls")
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
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
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
        route='privacy_policy/',
        view=TemplateView.as_view(template_name="privacy/privacy_policy.html"),
        name='privacy_policy'
    ),
    path(
        route='dashboard/',
        view=include("dashboard.urls"),
        name='dashboard'
    )
)
