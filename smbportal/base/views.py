#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf.global_settings import LOGIN_URL
from django.views.generic.edit import CreateView,View



def index(request):
    return render(request, "base/home.html")






