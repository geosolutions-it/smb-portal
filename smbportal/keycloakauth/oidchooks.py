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
    """Process additional scope values in the token"""

    logger.debug("-- update_user_data called")
    keycloak_groups = token.get("groups", [])
    groups = []
    group_mappings = settings.KEYCLOAK.get("group_mappings", {})
    for group_path in keycloak_groups:
        if group_path in group_mappings.values():
            groups.append(group_path)
    revoke_stale_memberships(user, groups)
    create_django_memberships(user, groups)


def load_user_roles(user, roles):
    logger.debug("-- load_user_roles called")
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


def revoke_stale_memberships(user: AbstractUser, group_paths: Iterable):
    """Remove user from django groups that are not specified in keycloak"""
    logger.debug("Revoking stale memberships for user {}...".format(user))
    allowed_group_names = [path.rpartition("/")[-1] for path in group_paths]
    for group in user.groups.exclude(name__in=allowed_group_names):
        user.groups.remove(group)
    user.save()


def create_django_memberships(user: AbstractUser, group_paths: Iterable):
    """Add user to django groups that are specified in keycloak

    This function will create new django groups if they do not exist yet

    """

    logger.debug("Creating new memberships for user {}...".format(user))
    allowed_group_names = [path.rpartition("/")[-1] for path in group_paths]
    for group_name in allowed_group_names:
        group = Group.objects.get_or_create(name=group_name)[0]
        user.groups.add(group)
    user.save()
