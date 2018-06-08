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

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from profiles.rules import has_profile

logger = logging.getLogger(__name__)


def index(request):
    user = request.user
    if user.is_authenticated and not has_profile(user):
        messages.warning(
            request,
            "Please complete your profile before continuing to use the portal"
        )
        return redirect("profile:create")
    return render(request, "base/home.html")
