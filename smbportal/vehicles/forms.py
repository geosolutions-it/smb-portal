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
from django.utils.text import mark_safe
from django.utils.text import slugify
from photologue.models import Photo

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


class BikePossessionHistoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        bike = kwargs.pop("bike", None)
        super().__init__(*args, **kwargs)
        self.instance.reporter = user
        if bike is not None:
            self.instance.bike = bike
            del self.fields["bike"]
        else:
            self.fields["bike"].queryset = models.Bike.objects.filter(
                owner=user)

    class Meta:
        model = models.BikePossessionHistory
        fields = (
            "bike",
            "possession_state",
            "details",
        )
        widgets = {
            "possession_state": forms.RadioSelect,
        }


class BikePictureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike", None)
        super().__init__(*args, **kwargs)
        self.instance.gallery = self.bike.picture_gallery

    def clean(self):
        """Perform validation of fields that depend on each other

        We are re-implementing this method because the photologue ``Photo``
        model requires a unique ``slug`` field for an uploaded photo. Since
        we chose not to include this field in the upload form, but to
        construct it dynamically instead, we need to validate it before it
        reaches the DB (where it will fail if the slug is not unique)

        """

        super().clean()
        file_name = self.cleaned_data["image"].name
        title = "-".join((str(self.bike.pk), file_name))
        slugged_title = slugify(title)
        gallery = self.bike.picture_gallery
        if gallery.photos.filter(slug=slugged_title).exists():
            # FIXME: should be passing "image" as the ``field`` value here
            #        However, that makes the template render a non-styled
            #        message next to the failing field. By passing ``None``
            #        we are at least rendering a correctly styled error in the
            #        template
            self.add_error(None, "Already uploaded a picture with that name")
        else:
            self.instance.title = title

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.title)
        return super().save(commit=commit)

    class Meta:
        model = Photo
        fields = (
            "image",
            "caption",
        )


class BikePictureDeleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        bike = kwargs.pop("bike")
        super().__init__(*args, **kwargs)
        choices = []
        for picture in bike.picture_gallery.photos.all():
            display_url = picture.get_thumbnail_url()
            render_as = mark_safe(
                '<img src="{}" alt="{}">'.format(display_url, picture.title))
            choices.append((picture.pk, render_as))

        self.fields["choices"] = forms.MultipleChoiceField(
            label="Choices",
            choices=choices,
            widget=forms.CheckboxSelectMultiple,
            error_messages={
                "required": "Must select at least one picture to delete",
            }
        )
