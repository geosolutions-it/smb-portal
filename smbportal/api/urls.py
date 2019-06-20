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

from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework import routers
from rest_framework.permissions import AllowAny

from badges.api import views as badges_views
from prizes.api import views as prizes_views
from profiles.api.urls import urlpatterns as profiles_urlpatterns
from profiles.api import views as profiles_views
from tracks.api import views as tracks_views
from vehiclemonitor.api import views as vehiclemonitor_views
from vehicles.api import views as vehicles_views

app_name = "api"

router = routers.DefaultRouter()
router.register(
    prefix="my-devices",
    viewset=FCMDeviceAuthorizedViewSet,
    base_name="my-devices"
)
router.register(
    prefix="my-badges",
    viewset=badges_views.MyBadgeViewSet,
    base_name="my-badges"
)
router.register(
    prefix="badges",
    viewset=badges_views.BadgeViewSet,
    base_name="badges"
)
router.register(
    prefix="my-competitions-won",
    viewset=prizes_views.MyCompetitionWonViewSet,
    base_name="my-competitions-won"
)
router.register(
    prefix="my-competitions-current",
    viewset=prizes_views.MyCurrentCompetitionViewSet,
    base_name="my-competitions-current"
)
router.register(
    prefix="competitions",
    viewset=prizes_views.CompetitionViewSet,
    base_name="competitions"
)
router.register(
    prefix="users",
    viewset=profiles_views.SmbUserViewSet,
    base_name="users"
)
router.register(
    prefix="my-segments",
    viewset=tracks_views.MySegmentViewSet,
    base_name="my-segments"
)
router.register(
    prefix="my-tracks",
    viewset=tracks_views.MyTrackViewSet,
    base_name="my-tracks"
)
router.register(
    prefix="tracks",
    viewset=tracks_views.TrackViewSet,
    base_name="tracks"
)
router.register(
    prefix="segments",
    viewset=tracks_views.SegmentViewSet,
    base_name="segments"
)
router.register(
    prefix="my-bike-observations",
    viewset=vehiclemonitor_views.MyBikeObservationViewSet,
    base_name="my-bike-observations"
)
router.register(
    prefix="bike-observations",
    viewset=vehiclemonitor_views.BikeObservationViewSet,
    base_name="bike-observations"
)
router.register(
    prefix="my-bikes",
    viewset=vehicles_views.MyBikeViewSet,
    base_name="my-bikes"
)
router.register(
    prefix="my-tags",
    viewset=vehicles_views.MyPhysicalTagViewSet,
    base_name="my-tags"
)
router.register(
    prefix="my-bike-statuses",
    viewset=vehicles_views.MyBikeStatusViewSet,
    base_name="my-bike-statuses"
)
router.register(
    prefix="bikes",
    viewset=vehicles_views.BikeViewSet,
    base_name="bikes"
)
router.register(
    prefix="bike-statuses",
    viewset=vehicles_views.BikeStatusViewSet,
    base_name="bike-statuses"
)
router.register(
    prefix="tags",
    viewset=vehicles_views.PhysicalTagViewSet,
    base_name="tags"
)

schema_view = get_schema_view(
    info=openapi.Info(
        title="",
        default_version="v1",
        description="SaveMyBike Platform API",
        terms_of_service="",
        contact=openapi.Contact(email="info@savemybike.eu"),
        license=openapi.License(name="BSD License"),
    ),
    url="{}/api".format(settings.KEYCLOAK["client_public_uri"]),
    public=False,
    permission_classes=[
        AllowAny,
    ]
)

urlpatterns = router.urls + profiles_urlpatterns + [
    path(
        route=r"swagger/",
        view=schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
]
