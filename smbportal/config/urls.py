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

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'^$', include("profiles.urls")),
)
