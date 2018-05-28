#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from . import forms

from . import models
from django.forms.widgets import TextInput


class UserActionMixin(object):

    @property
    def success_message(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        return super().form_valid(form)


class UserProfileMixin(object):

    def get_object(self, queryset=None):
        return self.request.user.profile


class EndUserDetailView(UserProfileMixin, DetailView):
    model = models.EndUserProfile
    

class EndUserCreateView(UserProfileMixin, UserActionMixin, CreateView):
    model = models.EndUserProfile
    context_object_name = "enduserprofile"
    form_class = forms.EndUserDetailViewForm
#     fields = (
#         "gender",
#     )
    template_name_suffix = "_create"
    success_message = "user profile created!"
    success_url = "create/survey"
    
    def get_initial(self):
        return { 'user': self.request.user }


class EndUserUpdateView(UserProfileMixin, UserActionMixin, UpdateView):
    model = models.EndUserProfile
    fields = (
        "gender",
    )
    template_name_suffix = "_update"
    success_message = "user profile updated!"
    

class EndUserSurvey(UserProfileMixin,UserActionMixin,CreateView):
    model = models.MobilityHabitsSurvey
    context_object_name="survey"
    form_class = forms.UserMobilityHabitsForm
    template_name_suffix = "_create"
    success_url = "/"
    
    def get_initial(self):
        return { 'user': self.request.user }
    
    
