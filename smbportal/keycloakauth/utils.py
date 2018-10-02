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
from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from bossoidc.models import Keycloak
from requests.exceptions import HTTPError

from base.utils import get_group_name
from profiles.models import SmbUser

from . import oidchooks
from .keycloakadmin import get_manager

logger = logging.getLogger(__name__)


def create_user(username, email, password, group_path, keycloak_manager,
                profile_model=None, profile_kwargs=None):
    """Create a new user on keycloak and on django DB"""
    user_id = create_keycloak_user(keycloak_manager, username, email,
                                   password, group_path)
    django_user = create_django_user(
        username, email, user_id, get_group_name(group_path),
        user_profile_model=profile_model,
        user_profile_kwargs=profile_kwargs
    )
    return django_user


def delete_user(username, keycloak_manager):
    """Delete user from django and from keycloak"""

    user = get_user_model().objects.get(username=username)
    keycloak_id = user.keycloak.UID
    try:
        keycloak_manager.delete_user(keycloak_id)
    except HTTPError as exc:
        logger.warning("Could not delete user {!r} from keycloak. Reason: "
                       "{}".format(keycloak_id, str(exc)))
    user.delete()


def create_keycloak_user(keycloak_manager, username, email,
                         password, group_path):
    """Create a user on keycloak and assign it the specified group"""
    keycloak_manager.create_user(username, email=email, password=password)
    user_id = keycloak_manager.get_user_details(username)["id"]
    keycloak_manager.add_user_to_group(user_id, group_path)
    return user_id


def create_django_user(username, email, keycloak_id, group_name,
                       user_profile_model=None, user_profile_kwargs=None):
    """Create a new django user and setup its keycloak id and groups"""
    user = get_user_model().objects.create(
        username=username, email=email)
    Keycloak.objects.create(user=user, UID=keycloak_id)
    group = Group.objects.get_or_create(name=group_name)[0]
    group.user_set.add(user)
    group.save()
    if user_profile_model is not None:
        kwargs = user_profile_kwargs if user_profile_kwargs is not None else {}
        user_profile_model.objects.create(
            user=user,
            **kwargs
        )
    return user


def update_user_groups(user: SmbUser, user_profile: str,
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
        keycloak_manager = get_manager(
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
