#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################


from django import forms
from django.utils.translation import gettext as _

from vehicles.models import Bike


class SegmentDownloadForm(forms.Form):
    start_date = forms.DateTimeField(
        label=_("Start date"),
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "class": "time_picker date_time_picker"
            }
        )
    )
    end_date = forms.DateTimeField(
        label=_("End date"),
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "class": "date_time_picker"
            }
        )
    )



class ObservationDownloadForm(forms.Form):
    start_date = forms.DateTimeField(
        label=_("Start date"),
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "class": "date_time_picker"
            }
        )
    )
    end_date = forms.DateTimeField(
        label=_("End date"),
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "class": "date_time_picker"
            }
        )
    )
    bikes = forms.ModelMultipleChoiceField(
        label=_("Bikes"),
        required=False,
        queryset=Bike.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "select_2 select_2_multiple"
            }
        )
    )
