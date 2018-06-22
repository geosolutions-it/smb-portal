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

from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from rest_framework.permissions import AllowAny

from . import views

app_name = "api"

router = routers.DefaultRouter()
router.register(
    prefix="my-bikes",
    viewset=views.MyBikeViewSet,
    base_name="my-bikes"
)
router.register(
    prefix="my-tags",
    viewset=views.MyPhysicalTagViewSet,
    base_name="my-tags"
)
router.register(
    prefix="my-bike-statuses",
    viewset=views.MyBikeStatusViewSet,
    base_name="my-bike-statuses"
)
router.register(
    prefix="my-bike-observations",
    viewset=views.MyBikeObservationViewSet,
    base_name="my-bike-observations"
)
router.register(
    prefix="users",
    viewset=views.SmbUserViewSet,
    base_name="users"
)
router.register(
    prefix="bikes",
    viewset=views.BikeViewSet,
    base_name="bikes"
)
router.register(
    prefix="tags",
    viewset=views.PhysicalTagViewSet,
    base_name="tags"
)
router.register(
    prefix="bike-statuses",
    viewset=views.BikeStatusViewSet,
    base_name="bike-statuses"
)
router.register(
    prefix="picture-galleries",
    viewset=views.GalleryViewSet,
    base_name="picture-galleries"
)
router.register(
    prefix="pictures",
    viewset=views.PictureViewSet,
    base_name="pictures"
)
router.register(
    prefix="bike-observations",
    viewset=views.BikeObservationViewSet,
    base_name="bike-observations"
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
    url="{}/api".format(settings.KEYCLOAK["client_public_uri"]),
    public=False,
    permission_classes=[
        AllowAny,
    ]
)

urlpatterns = [
    path(
        route=r"swagger/",
        view=schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
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
] + router.urls
