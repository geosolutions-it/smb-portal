#########################################################################
#
# Copyright 2019, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Custom fields for smb-portal"""

from django import forms
from django.contrib.postgres.fields import ArrayField

from .widgets import ArrayFieldSelectMultipleWidget


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
            "widget": ArrayFieldSelectMultipleWidget,
        }
        defaults.update(kwargs)
        # here we are calling ``formfield()`` of the ancestor class of
        # ``ArrayField``, i.e. we do not call ``ÀrrayField.formfield`` at all.
        # More info at:
        # https://gist.github.com/danni/f55c4ce19598b2b345ef#gistcomment-2041847
        return super(ArrayField, self).formfield(**defaults)
