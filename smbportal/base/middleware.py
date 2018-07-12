#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Custom django middleware for smbportal"""

import logging

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.utils import timezone
from ipware import get_client_ip
import pytz

logger = logging.getLogger(__name__)


def get_timezone(request, geoip):
    request_ip, is_routable = get_client_ip(
        request,
        **getattr(settings, "IPWARE", {})
    )
    logger.debug(
        "request_ip: {} - is_routable: {}".format(request_ip, is_routable))
    if request_ip is None:
        timezone = settings.TIME_ZONE
    else:
        city = geoip.city(request_ip)
        timezone = city.get("time_zone", settings.TIME_ZONE)
    return timezone


class TimezoneMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip = GeoIP2()

    def __call__(self, request):
        current_timezone = request.session.get("user_time_zone", None)
        if current_timezone is None:
            current_timezone = get_timezone(request, self.geoip)
            request.session["user_time_zone"] = current_timezone
        logger.debug("current_timezone: {}".format(current_timezone))
        timezone.activate(pytz.timezone(current_timezone))
        response = self.get_response(request)
        return response
