#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""django-rest-framework permission utilities"""

import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


def filter_out_unsafe_permissions(permissions_to_check):
    unsafe_words = [
        "create",
        "new",
        "edit",
        "update",
        "change",
        "delete",
        "remove",
    ]
    filtered = []
    for perm in permissions_to_check:
        for word in unsafe_words:
            if word in perm:
                break
        else:
            filtered.append(perm)
    return filtered


class DjangoRulesPermission(permissions.BasePermission):

    def _get_view_permissions(self, view):
        return getattr(view, "required_permissions", [])

    def _get_view_object_permissions(self, view):
        object_permissions = getattr(view, "required_object_permissions", None)
        if object_permissions is None:
            result = self._get_view_permissions(view)
        else:
            result = object_permissions
        return result

    def has_permission(self, request, view):

        """Check permissions for accessing the input view

        This method will by default deny access unless permissions are
        explicitly granted.

        """

        all_perms = self._get_view_permissions(view)
        safe_perms = filter_out_unsafe_permissions(all_perms)
        is_safe_method = request.method in permissions.SAFE_METHODS
        perms_to_check = safe_perms if is_safe_method else all_perms
        result = False
        if isinstance(perms_to_check, str):
            result = request.user.has_perm(perms_to_check)
        else:
            for perm in perms_to_check:
                if request.user.has_perm(perm):
                    result = True
                else:
                    result = False
                    break
        return result

    def has_object_permission(self, request, view, obj):
        all_permissions = self._get_view_object_permissions(view)
        safe_permissions = filter_out_unsafe_permissions(all_permissions)
        is_safe_method = request.method in permissions.SAFE_METHODS
        for perm in (safe_permissions if is_safe_method else all_permissions):
            if not request.user.has_perm(perm, obj):
                result = False
                break
        else:
            result = True
        return result
