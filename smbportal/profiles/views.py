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
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView

from base import mixins
from base import utils
from keycloakauth import oidchooks
from keycloakauth.keycloakadmin import get_manager as get_keycloak_manager
from . import forms
from . import models
from .rules import has_profile

logger = logging.getLogger(__name__)


def activate_language(language_code, request):
    logger.debug("activate_language called")
    translation.activate(language_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = language_code


def update_user_groups(user: models.SmbUser, user_profile: str,
                       current_keycloak_groups: List[str]):
    """Update a user's groups based on the requested user profile

    The workflow is:

    - user asks Keycloak to become a member of the group(s) corresponding
      to its profile
    - Keycloak either accepts and creates the memberships or denies and
      notifies an admin that user wants to be given membership of said groups
    - if Keycloak created the relevant memberships, we update the user's
      django groups

    Note:

    We do not use permissions here because we want Keycloak to be the
    authority on the user group memberships. In order to do that we can only
    update a django user's django group when we are certain that Keycloak
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
        keycloak_manager = get_keycloak_manager(
            base_url=settings.KEYCLOAK["base_url"],
            realm=settings.KEYCLOAK["realm"],
            client_id=settings.KEYCLOAK["client_id"],
            username=settings.KEYCLOAK["admin_username"],
            password=settings.KEYCLOAK["admin_password"],
        )
        if user_profile == settings.END_USER_PROFILE:
            missing_memberships = set(
                memberships_to_enforce) - set(current_groups)
            if any(missing_memberships):
                for group_path in missing_memberships:
                    keycloak_manager.add_user_to_group(user_id, group_path)
            result = memberships_to_enforce
        else:
            keycloak_manager.set_user_access(user_id, enabled=False)
            raise RuntimeError("profiles of type {!r} must be manually "
                               "approved by an admin".format(user_profile))
    return result


class UserProfileMixin(object):

    def get_object(self, queryset=None):
        user = self.request.user
        return user.profile if has_profile(user) else False


class PrivilegedUserProfileCreateView(LoginRequiredMixin,
                                      PermissionRequiredMixin,
                                      UserProfileMixin,
                                      mixins.FormUpdatedMessageMixin,
                                      CreateView):
    model = models.PrivilegedUserProfile
    template_name_suffix = "_create"
    success_url = settings.LOGOUT_URL
    permission_required = "profiles.can_create_profile"
    fields = ()
    admin_email_subject_template_name = (
        "profiles/mail/privilegeduser_registration_request_subject.txt")
    admin_email_message_template_name = (
        "profiles/mail/privilegeduser_registration_request_message.txt")

    @property
    def success_message(self):
        return _("Privileged user profile created!")

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["user_form"] = self._get_user_form()
        return context_data

    def form_valid(self, form):
        """Assign the request's user to the form and perform profile moderation

        This method relies on the presence of a ``groups`` key on the id token.

        """

        form.instance.user = self.request.user
        user_form = self._get_user_form()
        if user_form.is_valid():
            user = user_form.save()
            activate_language(user.language_preference, self.request)
            super().form_valid(form)
            id_token = self.request.session.get("id_token")
            try:
                update_user_groups(
                    user=self.request.user,
                    user_profile=settings.PRIVILEGED_USER_PROFILE,
                    current_keycloak_groups=id_token.get("groups", [])
                )
                result = redirect("home")
            except RuntimeError:
                messages.info(
                    self.request, _("Registration request sent to admins"))
                messages.info(self.request, _("You have been logged out"))
                utils.send_email_to_admins(
                    self.admin_email_subject_template_name,
                    self.admin_email_message_template_name,
                    context={
                        "username": self.request.user.username,
                        "email": self.request.user.email,
                        "keycloak_base_url": settings.KEYCLOAK["base_url"],
                        "site_name": get_current_site(self.request),
                    }
                )
                result = redirect(settings.LOGOUT_URL)
        else:
            result = self.form_invalid(form)
        return result

    def form_invalid(self, form):
        user_form = self._get_user_form()
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form))

    def _get_user_form(self):
        data = self.request.POST if self.request.method == "POST" else None
        return forms.SmbUserForm(data=data, instance=self.request.user)


class EndUserProfileCreateView(LoginRequiredMixin,
                               PermissionRequiredMixin,
                               UserProfileMixin,
                               mixins.FormUpdatedMessageMixin,
                               CreateView):
    """Profile completion view

    This view uses two forms, one for the completion of the user profile and
    another for the mobility habits survey.

    """

    model = models.EndUserProfile
    form_class = forms.EndUserProfileForm
    template_name_suffix = "_create"
    permission_required = "profiles.can_create_profile"
    success_url = reverse_lazy("bikes:list")

    @property
    def goto(self):
        return "bikes:list"

    @property
    def success_message(self):
        return _("User profile created. You can now add some bikes")

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        elif has_profile(self.request.user):
            raise PermissionDenied("User already has a profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._get_extra_forms())
        return context

    def form_valid(self, form):
        """Assign the request's user to the form and perform profile moderation

        This method relies on the presence of a ``groups`` key on the id token.
        This key is used in order to sync group memberships with keycloak.

        """

        form.instance.user = self.request.user
        # validate extra forms before saving anything
        extra_forms = self._get_extra_forms()
        if all([f.is_valid() for f in extra_forms.values()]):
            super().form_valid(form)
            # upon calling super().form_valid(form) the property self.object
            # points to the newly created enduser profile
            mobility_form = extra_forms["mobility_form"]
            mobility_form.instance.end_user = self.object
            mobility_form.save()
            user_form = extra_forms["user_form"]
            user = user_form.save()
            activate_language(user.language_preference, self.request)
            response = redirect(self.get_success_url())
            id_token = self.request.session.get("id_token")
            update_user_groups(
                user=self.request.user,
                user_profile=settings.END_USER_PROFILE,
                current_keycloak_groups=id_token.get("groups", [])
            )
        else:
            response = self.form_invalid(form)
        logger.debug("response: {}".format(response))
        return response

    def form_invalid(self, form):
        extra_forms = self._get_extra_forms()
        return self.render_to_response(
            self.get_context_data(form=form, **extra_forms))

    def _get_extra_forms(self):
        data = self.request.POST if self.request.method == "POST" else None
        return {
            "user_form": forms.SmbUserForm(data=data,
                                           instance=self.request.user),
            "mobility_form": forms.UserMobilityHabitsForm(data=data)
        }


class ProfileUpdateView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        mixins.UserHasObjectPermissionMixin,
                        UserProfileMixin,
                        mixins.FormUpdatedMessageMixin,
                        UpdateView):
    permission_required = "profiles.can_edit_profile"

    @property
    def success_message(self):
        return _("User profile updated!")


    def has_permission(self):
        user = self.request.user
        for perm in self.get_permission_required():
            if not user.has_perm(perm, obj=user.profile):
                result = False
                break
        else:
            result = True
        return result

    def get_template_names(self):
        profile_class = type(self.request.user.profile)
        template_name = {
            models.EndUserProfile: "profiles/enduserprofile_update.html",
            models.PrivilegedUserProfile: (
                "profiles/privilegeduserprofile_update.html"),
        }.get(profile_class)
        return [template_name]

    def get_queryset(self):
        profile_class = type(self.request.user.profile)
        return profile_class.objects.get(pk=self.request.user.profile.pk)

    def get_form_class(self):
        profile_class = type(self.request.user.profile)
        return {
            models.EndUserProfile: forms.EndUserProfileForm,
            models.PrivilegedUserProfile: forms.PrivilegedUserProfileForm,
        }.get(profile_class)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["user_form"] = self._get_user_form()
        return context_data

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            result = settings.LOGIN_URL
        else:
            messages.info(
                self.request,
                _("Please complete your user profile before continuing")
            )
            result = reverse("profile:create")
        return result

    def form_valid(self, form):
        """Process uploaded form data after the form has been validated

        Reimplemented in order to also perform validation on the other form,
        for the SmbUser model, and handle all uploaded data.

        """

        form.instance.user = self.request.user
        user_form = self._get_user_form()
        if user_form.is_valid():
            user = user_form.save()
            activate_language(user.language_preference, self.request)
            response = super().form_valid(form)
        else:
            response = self.form_invalid(form)
        return response

    def form_invalid(self, form):
        user_form = self._get_user_form()
        return self.render_to_response(
            self.get_context_data(form=form, user_form=user_form))

    def _get_user_form(self):
        data = self.request.POST if self.request.method == "POST" else None
        return forms.SmbUserForm(
            data=data,
            instance=self.request.user,
            include_accept_terms_field=False
        )


class MobilityHabitsSurveyCreateView(LoginRequiredMixin,
                                     PermissionRequiredMixin,
                                     UserProfileMixin,
                                     mixins.FormUpdatedMessageMixin,
                                     CreateView):
    model = models.MobilityHabitsSurvey
    context_object_name = "survey"
    form_class = forms.UserMobilityHabitsForm
    template_name_suffix = "_create"
    success_url = reverse_lazy("profile:update")
    permission_required = "profiles.can_edit_profile"

    def has_permission(self):
        user = self.request.user
        for perm in self.get_permission_required():
            if not user.has_perm(perm, obj=user.profile):
                result = False
                break
        else:
            result = True
        return result

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_URL
        else:
            raise PermissionDenied()

    def form_valid(self, form):
        form.instance.end_user = self.request.user.profile
        return super().form_valid(form)


class MobilityHabitsSurveyDetailView(LoginRequiredMixin,
                                     PermissionRequiredMixin,
                                     mixins.AjaxTemplateMixin,
                                     DetailView):
    model = models.MobilityHabitsSurvey
    context_object_name = "survey"
    permission_required = "profiles.can_view_profile"
    ajax_template_name = "profiles/mobilityhabitssurvey_detail_inner.html"
