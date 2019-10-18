#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from profiles import rules

logger = logging.getLogger(__name__)


def index(request):
    user = request.user
    if user.is_authenticated and not rules.has_profile(user):
        messages.warning(
            request,
            "Please complete your profile before continuing to use the portal"
        )
        result = redirect("profile:create")
    elif user.is_authenticated and rules.is_privileged_user(user):
        result = redirect("dashboard:index")
    else:
        result = render(request, "base/home.html")
    return result
