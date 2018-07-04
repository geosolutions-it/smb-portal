#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Custom widgets for smb-portal"""

from django.contrib.gis.forms.widgets import OSMWidget


class SmbOsmWidget(OSMWidget):
    template_name = "gis/widgets/openlayers-osm.html"

    class Media:
        # set to False in order to prevent synchronous XHR requests when
        # including this widget on a form that is loaded via ajax
        # - the template is responsible for loading the openlayers css and js
        #   assets
        extend = False
