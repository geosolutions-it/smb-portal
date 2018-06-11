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

from django import forms

from . import models

logger = logging.getLogger(__name__)


class BikeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):
        """Perform validation of fields that depend on each other

        Notes
        -----
        Theoretically this method should not need to be re-implemented because
        we already defined a unique_together(owner, nickname) constraint on
        the ``Bike`` model. Usually a ModelForm runs uniqueness constraints on
        the model in its _post_clean method() and takes care of raising
        ``ValidationError`` if a unique constraint fails (this also includes
        unique_together). However, in this particular case, we set up our
        uniqueness with a field that is not part of the form's fields, since
        we set the bike's owner to be the current request's user.
        The django implementation of validating uniqueness actually excludes
        any fields that are not part of the form from its process. This means
        that our unique_together constraint is not validated during the usual
        form.is_valid() stuff.

        If a user chooses an already existing nickname, the uniqueness
        constraint still fails, but this happens only at the DB layer, which
        comes after form validation. This would result in an ``IntegrityError``
        being raised in the view(s) that use this form class.

        In order to prevent having to do another layer of validation inside
        the view we are doing the uniqueness validation here.

        """

        super().clean()
        nickname = self.cleaned_data.get("nickname")
        if self.user.bikes.filter(nickname=nickname).exclude(
                id=self.instance.id).exists():
            # FIXME: should be passing "nickname" as the ``field`` value here
            #        However, that makes the template render a non-styled
            #        message next to the failing field. By passing ``None``
            #        we are at least rendering a correctly styled error in the
            #        template
            self.add_error(
                None, "A bike with that nickname already exists")

    def save(self, commit=True):
        self.instance.owner = self.user
        return super().save(commit=commit)

    class Meta:
        model = models.Bike
        fields = (
            "nickname",
            "bike_type",
            "gear",
            "brake",
            "brand",
            "model",
            "color",
            "saddle",
            "has_basket",
            "has_cargo_rack",
            "has_lights",
            "has_bags",
            "has_smb_sticker",
            "other_details",
        )
