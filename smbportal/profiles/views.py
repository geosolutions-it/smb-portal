#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from typing import List
import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from base import mixins
from keycloakauth import oidchooks
from keycloakauth.keycloakadmin import KeycloakManager
from . import forms
from . import models
from .rules import has_profile

logger = logging.getLogger(__name__)


def update_user_groups(user: models.SmbUser, user_profile: str,
                       current_keycloak_groups: List[str]):
    """Update a user's groups based on the requested user profile

    The workflow is:

    - user asks KeyCloak to become a member of the group(s) corresponding
      to its profile
    - KeyCloak either accepts and creates the memberships or denies and
      notifies an admin that user wants to be given membership of said groups
    - if KeyCloak created the relevant memberships, we update the user's
      django groups

    Note:

    We do not use permissions here because we want keycloak to be the
    authority on the user group memberships. In order to do that we can only
    update a django user's django group when we are certain that keycloak
    already has reflected that membership in its own user database

    """

    keycloak_groups = enforce_keycloak_group_memberships(
        user.keycloak.UID,
        user_profile,
        current_keycloak_groups
    )
    oidchooks.create_django_memberships(user, keycloak_groups)


def enforce_keycloak_group_memberships(user_id: str, user_profile: str,
                                       current_groups: List[str]):
    """Assign user memberships on the relevant KeyCloak groups, if allowed.

    The registration of some user profiles, like `end_user`, is automatically
    accepted, resulting in the relevant KeyCloak groups needing to be updated
    with new members. Other profile types are not allowed to self register as
    group members on KeyCloak.

    """

    memberships_to_enforce = settings.KEYCLOAK["group_mappings"][user_profile]
    if set(current_groups) == set(memberships_to_enforce):
        result = current_groups
    else:
        keycloak_manager = KeycloakManager(
            base_url=settings.KEYCLOAK["base_url"],
            realm=settings.KEYCLOAK["realm"],
            admin_username=settings.KEYCLOAK["admin_username"],
            admin_password=settings.KEYCLOAK["admin_password"],
        )
        if user_profile == settings.END_USER_PROFILE:
            missing_memberships = set(current_groups) - set(
                memberships_to_enforce)
            if any(missing_memberships):
                for group_path in missing_memberships:
                    keycloak_manager.add_user_to_group(user_id, group_path)
            result = memberships_to_enforce
        else:
            keycloak_manager.set_user_access(user_id, enabled=False)
            raise RuntimeError("profiles of type {!r} must be manually "
                               "approved by an admin".format(user_profile))
    return result


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


class PrivilegedUserProfileCreateView(LoginRequiredMixin,
                                      PermissionRequiredMixin,
                                      UserProfileMixin,
                                      FormUpdatedMessageMixin,
                                      CreateView):
    model = models.PrivilegedUserProfile
    template_name_suffix = "_create"
    success_message = "privileged-user profile created!"
    success_url = settings.LOGOUT_URL
    permission_required = "profiles.can_create"
    fields = ()

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")

    def form_valid(self, form):
        """Assign the request's user to the form and perform profile moderation

        This method relies on the presence of a ``groups`` key on the id token.

        """

        form.instance.user = self.request.user
        super().form_valid(form)
        id_token = self.request.session.get("id_token")
        logger.debug(
            "current_keycloak_groups: {}".format(id_token.get("groups", [])))
        try:
            update_user_groups(
                user=self.request.user,
                user_profile=settings.PRIVILEGED_USER_PROFILE,
                current_keycloak_groups=id_token.get("groups", [])
            )
            result = redirect("home")
        except RuntimeError:
            messages.info(self.request, "Registration request sent to admins")
            messages.info(self.request, "You have been logged out")
            logger.debug(
                "About to notify admin that user {!r} wants to register with "
                "role {!r}".format(self.request.user.username,
                                   settings.PRIVILEGED_USER_PROFILE)
            )
            result = redirect(settings.LOGOUT_URL)
        return result


class EndUserProfileCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UserProfileMixin,
                               FormUpdatedMessageMixin,
                               CreateView):
    model = models.EndUserProfile
    form_class = forms.EndUserProfileForm
    template_name_suffix = "_create"
    success_message = "end-user profile created!"
    permission_required = "profiles.can_create"
    success_url = reverse_lazy("profile:create-survey")

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mobility_form"] = forms.UserMobilityHabitsForm()
        return context

    def form_valid(self, form):
        """Assign the request's user to the form and perform profile moderation

        This method relies on the presence of a ``groups`` key on the id token.

        """

        form.instance.user = self.request.user
        response = super().form_valid(form)
        id_token = self.request.session.get("id_token")
        logger.debug(
            "current_keycloak_groups: {}".format(id_token.get("groups", [])))
        update_user_groups(
            user=self.request.user,
            user_profile=settings.END_USER_PROFILE,
            current_keycloak_groups=id_token.get("groups", [])
        )
        return response



class ProfileUpdateView(LoginRequiredMixin,
                        mixins.UserHasObjectPermissionMixin,
                        PermissionRequiredMixin,
                        UserProfileMixin,
                        FormUpdatedMessageMixin,
                        UpdateView):
    permission_required = "profiles.can_edit"
    success_message = "user profile updated!"

    def get_template_names(self):
        profile_class = type(self.request.user.profile)
        template_name = {
            models.EndUserProfile: "profiles/enduserprofile_update.html",
            models.PrivilegedUserProfile: (
                "profiles/privilegeduserprofile_update.html"),
        }.get(profile_class)
        return [template_name]

    def get_queryset(self):
        logger.debug("On the get_queryset method of ProfileUpdateView")
        print("On the get_queryset method of ProfileUpdateView")
        profile_class = type(self.request.user.profile)
        return profile_class.objects.get(pk=self.request.user.profile.pk)

    def get_form_class(self):
        logger.debug("On the get_form_class method of ProfileUpdateView")
        print("On the get_form_class method of ProfileUpdateView")
        profile_class = type(self.request.user.profile)
        return {
            models.EndUserProfile: forms.EndUserProfileForm,
            models.PrivilegedUserProfile: forms.PrivilegedUserProfileForm,
        }.get(profile_class)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            result = settings.LOGIN_URL
        else:
            result = reverse("profile:create")
        return result

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
