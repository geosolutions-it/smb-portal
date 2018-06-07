#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Extra tags for using in smb-portal templates"""

from django import template

register = template.Library()


@register.filter
def add_str(arg1, arg2):
    """Concatenate input args"""
    return "".join((str(arg1), str(arg2)))