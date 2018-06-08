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


class DjangoRulesPermission(permissions.BasePermission):

    def _get_view_permissions(self, view):
        return getattr(view, "required_permissions", [])

    def _get_view_object_permissions(self, view):
        object_permissions = getattr(view, "required_object_permissions", None)
        if object_permissions is None:
            return self._get_view_permissions(view)

    def has_permission(self, request, view):
        permissions = self._get_view_permissions(view)
        user = request.user
        for perm in permissions:
            if not user.has_perm(perm):
                result = False
                break
        else:
            result = True
        return result

    def has_object_permission(self, request, view, obj):
        permissions = self._get_view_object_permissions(view)
        user = request.user
        for perm in permissions:
            if not user.has_perm(perm, obj):
                result = False
                break
        else:
            result = True
        return result
