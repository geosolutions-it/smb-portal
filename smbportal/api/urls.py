#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""URLs for the smb-portal's REST API"""

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.permissions import AllowAny

from . import views

app_name = "api"

router = routers.DefaultRouter()
router.register(
    prefix=r"users",
    viewset=views.SmbUserViewSet,
    base_name="users"
)
router.register(
    prefix=r"bikes",
    viewset=views.BikeViewSet,
    base_name="bikes"
)
router.register(
    prefix=r"tags",
    viewset=views.PhysicalTagViewSet,
    base_name="tags"
)
router.register(
    prefix=r"bike-possession-history",
    viewset=views.BikePossessionHistoryViewSet,
    base_name="bike-possession-history"
)
router.register(
    prefix=r"picture-galleries",
    viewset=views.GalleryViewSet,
    base_name="picture-galleries"
)
router.register(
    prefix=r"pictures",
    viewset=views.PictureViewSet,
    base_name="pictures"
)

schema_view = get_schema_view(
    info=openapi.Info(
        title="",
        default_version="v1",
        description="Test description",
        terms_of_service="",
        contact=openapi.Contact(email="fake@mail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        AllowAny,
    ]
)

urlpatterns = [
    path(
        route=r"swagger/",
        view=schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    )
] + router.urls