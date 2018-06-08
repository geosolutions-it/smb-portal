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

from django.contrib import messages

logger = logging.getLogger(__name__)


class FormUpdatedMessageMixin(object):

    @property
    def success_message(self):
        return NotImplemented

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.info(self.request, self.success_message)
        return result


class UserHasObjectPermissionMixin(object):

    def has_permission(self):
        """Test whether the current user has all required permissions

        This method has been reimplemented in order to provide object-level
        permission checks. The default django permissions implementation does
        not check permissions on individual objects. In this case we want
        to make sure a user can only gain access to his/her own profile.

        """

        logger.debug(
            "inside UserHasObjectPermissionMixin's has_permission method")
        current_user = self.request.user
        permissions_to_check = self.get_permission_required()
        return current_user.has_perms(
            permissions_to_check,
            obj=self.get_object()
        )
