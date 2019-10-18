#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""URLs for the smb-portal's REST API"""

from django.urls import path

from . import views

urlpatterns = [
    path(
        route="my-user",
        view=views.MyUserViewSet.as_view(
            actions={
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
            }
        ),
        name="my-user"
    )
]
