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

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from bossoidc.models import Keycloak
from requests.exceptions import HTTPError

from base.utils import get_group_name

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
