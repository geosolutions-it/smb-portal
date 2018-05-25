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

urlpatterns = [
    path('openid/', include('djangooidc.urls')),
]


urlpatterns += i18n_patterns(
    path(r'admin/', admin.site.urls),
    path(r'', include("profiles.urls")),
)
