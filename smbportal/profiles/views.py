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
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from . import forms

from . import models
from .rules import has_profile
from .rules import is_profile_owner

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


class EndUserProfileDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                               UserProfileMixin, DetailView):
    model = models.EndUserProfile
    context_object_name = "enduserprofile"
    form_class = forms.EndUserDetailViewForm
    permission_required = "profiles.can_view"
    object_level_permissions = True

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            result = settings.LOGIN_URL
        else:
            if not has_profile(self.request.user):
                result = reverse_lazy("profile:create")
            else:
                current_profile = self.get_object()
                if not is_profile_owner(self.request.user, current_profile):
                    raise PermissionDenied()
                else:
                    raise RuntimeError()
        return result

    def has_permission(self):
        """Test whether the current user has all required permissions

        This method has been reimplemented in order to provide object-level
        permission checks. The default django permissions implementation does
        not check permissions on individual objects. In this case we want
        to make sure a user can only gain access to his/her own profile.

        """

        current_user = self.request.user
        try:
            current_obj = self.request.user.profile
        except ObjectDoesNotExist:
            current_obj = None
        permissions_to_check = self.get_permission_required()
        return current_user.has_perms(permissions_to_check, obj=current_obj)


class EndUserProfileCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                               UserProfileMixin, FormUpdatedMessageMixin,
                               CreateView):
    model = models.EndUserProfile
    context_object_name = "enduserprofile"
    form_class = forms.EndUserCreateViewForm
#     fields = (
#         "gender",
#     )
    template_name_suffix = "_create"
    success_message = "user profile created!"
    permission_required = "profiles.can_create"
    success_url = "create/survey"

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")
        
        
    def get_initial(self):
        return { 'user': self.request.user }


class EndUserProfileUpdateView(LoginRequiredMixin, UserProfileMixin,
                               FormUpdatedMessageMixin, UpdateView):
    model = models.EndUserProfile
    fields = (
        "gender",
    )
    template_name_suffix = "_update"
    success_message = "user profile updated!"


class EndUserSurvey(UserProfileMixin, FormUpdatedMessageMixin,
                    CreateView):
    model = models.MobilityHabitsSurvey
    context_object_name="survey"
    form_class = forms.UserMobilityHabitsForm
    template_name_suffix = "_create"
    success_url = "/"

    def get_initial(self):
        return { 'user': self.request.user }
