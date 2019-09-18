#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""boss-oidc hook functions"""

import logging
from typing import Iterable

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)


def update_user_data(user, token):
    """Process additional scope values in the token

    This function is an extension hook of the
    ``bossoidc.backend.OpenIdConnectBackend`` class. It is executed everytime
    a user logs-in.

    """

    logger.debug("update_user_data called")
    keycloak_group_paths = token.get("groups", [])
    logger.debug("keycloak_group_paths: {}".format(keycloak_group_paths))
    group_mappings = settings.KEYCLOAK.get("group_mappings", {})
    groups = []
    for path in keycloak_group_paths:
        for django_group_name, path_list in group_mappings.items():
            if path in path_list:
                groups.append(path)
    logger.debug("django groups_to_act_upon: {}".format(groups))
    revoke_stale_memberships(user, groups)
    create_django_memberships(user, groups)
    update_user_details(user, token)


def update_user_details(user, token):
    user.first_name = token.get("given_name", user.first_name)
    user.last_name = token.get("family_name", user.last_name)
    user.username = token.get("preferred_username", user.username)
    user.email = token.get("email", user.email)
    user.save()


def load_user_roles(user, roles):
    """Load user roles defined in the OpenID Connect Provider.

    This function is an extension hook of the
    ``bossoidc.backend.OpenIdConnectBackend`` class. It is executed everytime
    a user logs-in.

    """

    logger.debug("load_user_roles called")
    logger.debug("user: {}".format(user))
    logger.debug("roles: {}".format(roles))
    filtered_roles = enforce_staff_role(user, enforce_admin_role(user, roles))
    for role in filtered_roles:
        # oidc_role = models.OidcRole.objects.get_or_create(name=role)[0]
        # models.UserRole.objects.get_or_create(role=oidc_role, user=user)
        pass

    # stale_roles_qs = models.UserRole.objects.filter(
    #     user=user).exclude(role__name__in=roles)
    # stale_roles_qs.delete()


def enforce_admin_role(user: AbstractUser, roles: list) -> list:
    """Synchronize django ``superuser`` role from the keycloak roles

    The returned list of roles does not contain the admin role anymore.

    """

    logger.debug("Enforcing admin role for user {}...".format(user))
    result = roles[:]
    try:
        result.remove(settings.KEYCLOAK.get("admin_role"))
        user.is_superuser = True
    except ValueError:
        user.is_superuser = False
    user.save()
    return result


def enforce_staff_role(user: AbstractUser, roles: list) -> list:
    """Synchronize django ``staff`` role from the keycloak roles

    The returned list of roles does not contain the staff role anymore.

    """
    logger.debug("Enforcing staff role for user {}...".format(user))
    result = roles[:]
    try:
        result.remove(settings.KEYCLOAK.get("staff_role"))
        user.is_staff = True
    except ValueError:
        user.is_staff = False
    user.save()
    return result


def revoke_stale_memberships(user: AbstractUser, group_paths: Iterable[str]):
    """Remove user from django groups that are not specified in keycloak"""
    logger.debug("Revoking stale memberships for user {}...".format(user))
    allowed_group_names = [path.rpartition("/")[-1] for path in group_paths]
    for group in user.groups.exclude(name__in=allowed_group_names):
        logger.debug("removing user {} from group {}...".format(user, group))
        user.groups.remove(group)
    user.save()


def create_django_memberships(user: AbstractUser, group_paths: Iterable[str]):
    """Add user to django groups that are specified in keycloak

    This function will create new django groups if they do not exist yet

    """

    logger.debug("Creating new django memberships for user {}...".format(user))
    allowed_group_names = [path.rpartition("/")[-1] for path in group_paths]
    for group_name in allowed_group_names:
        group = Group.objects.get_or_create(name=group_name)[0]
        logger.debug("adding user {} to group {}".format(user, group))
        user.groups.add(group)
    user.save()
