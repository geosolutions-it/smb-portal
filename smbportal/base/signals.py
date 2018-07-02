#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Signal handlers for the smb-portal"""

from django.utils import translation


def set_user_language(sender, request=None, **kwargs):
    user_language = request.user.language_preference
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language


