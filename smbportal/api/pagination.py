#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Custom pagination classes for the portal"""

from rest_framework.pagination import PageNumberPagination


class SmbUserDumpPageNumberPagination(PageNumberPagination):
    page_size = 500
