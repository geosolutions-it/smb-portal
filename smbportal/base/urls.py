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
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from . import views

urlpatterns = [
    path('openid/', include('djangooidc.urls')),
]


urlpatterns += i18n_patterns(
    path(
        route=r'admin/',
        view=admin.site.urls
    ),
    path(
        route=r'',
        view=views.index,
        name="index"
    ),
    path(
        route=r'profiles/',
        view=include("profiles.urls"),
        name="profiles"
    ),
)
