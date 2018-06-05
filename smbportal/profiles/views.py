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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from base import mixins
from . import forms
from . import models
from .rules import has_profile

logger = logging.getLogger(__name__)


class FormUpdatedMessageMixin(object):

    @property
    def success_message(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        return super().form_valid(form)


class UserProfileMixin(object):

    def get_object(self, queryset=None):
        user = self.request.user
        return user.profile if has_profile(user) else False


class EndUserProfileCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UserProfileMixin,
                               FormUpdatedMessageMixin,
                               CreateView):
    model = models.EndUserProfile
    form_class = forms.EndUserProfileForm
    template_name_suffix = "_create"
    success_message = "user profile created!"
    permission_required = "profiles.can_create"
    success_url = reverse_lazy("profile:create-survey")

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EndUserProfileUpdateView(LoginRequiredMixin,
                               mixins.UserHasObjectPermissionMixin,
                               PermissionRequiredMixin,
                               UserProfileMixin,
                               FormUpdatedMessageMixin,
                               UpdateView):
    model = models.EndUserProfile
    form_class = forms.EndUserProfileForm
    template_name_suffix = "_update"
    permission_required = "profiles.can_edit"
    success_message = "user profile updated!"

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        else:
            raise PermissionDenied("Not authorized to edit profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MobilityHabitsSurveyCreateView(LoginRequiredMixin,
                                     UserProfileMixin,
                                     FormUpdatedMessageMixin,
                                     CreateView):
    model = models.MobilityHabitsSurvey
    context_object_name = "survey"
    form_class = forms.UserMobilityHabitsForm
    template_name_suffix = "_create"
    success_url = reverse_lazy("profile:update")

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        form.instance.end_user = self.request.user.profile
        return super().form_valid(form)


class MobilityHabitsSurveyDetailView(LoginRequiredMixin,
                                     DetailView):
    model = models.MobilityHabitsSurvey
    context_object_name = "survey"
