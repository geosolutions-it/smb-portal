#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings
from django.http import HttpResponse


def index(request):
    print("Inside index view. Current user: {}".format(request.user))
    raw_response = """
    <p>Hi {user}</p>
    <a href=\"{login_url}\">login</a>
    <p>You're at the index.</p>
    <a href=\"{logout_url}\">logout</a>
    """.format(
        user=request.user,
        login_url="{}?next={}".format(
            settings.LOGIN_URL, request.get_full_path()),
        logout_url=settings.LOGOUT_URL,
    )
    return HttpResponse(raw_response)

