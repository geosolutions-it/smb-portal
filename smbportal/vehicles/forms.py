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

from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms import bootstrap
from django.conf import settings
from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.text import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext as _

from base import widgets
from . import models
from . import validators

logger = logging.getLogger(__name__)


class BikeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        is_ajax = kwargs.pop("is_ajax", None)
        action = kwargs.pop("action", None)
        submit_value = kwargs.pop("submit_value", "OK")
        super().__init__(*args, **kwargs)
        self.instance.owner = self.user
        self.helper = FormHelper(
        )
        self.helper.form_id = "bikeForm"
        if action is not None:
            self.helper.form_action = action
        self.helper.layout = layout.Layout(
            layout.Field("nickname"),
            layout.Div(
                layout.Div(
                    layout.Field("bike_type"),
                    css_class="col-lg-4",
                ),
                layout.Div(
                    layout.Field("gear"),
                    css_class="col-lg-4",
                ),
                layout.Div(
                    layout.Field("brake"),
                    css_class="col-lg-4",
                ),
                layout.Div(
                    layout.Field("brand"),
                    layout.Field("model"),
                    css_class="col-lg-6",
                ),
                layout.Div(
                    layout.Field("color"),
                    layout.Field("saddle"),
                    css_class="col-lg-6",
                ),
                layout.Div(
                    layout.Fieldset(
                        None,
                        "has_basket",
                        "has_cargo_rack",
                    ),
                    css_class="col-lg-6",
                ),
                layout.Div(
                    layout.Fieldset(
                        None,
                        "has_lights",
                        "has_bags",
                    ),
                    css_class="col-lg-6",
                ),
                css_class="row"
            ),
            layout.Field("other_details"),
        )
        if not is_ajax:
            self.helper.layout.append(
                bootstrap.FormActions(
                    layout.Submit("submit", submit_value)
                ),
            )

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
                None, _("A bike with that nickname already exists"))

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
            "other_details",
        )
        widgets = {
            "bike_type": forms.RadioSelect,
            "gear": forms.RadioSelect,
            "brake": forms.RadioSelect,
        }


class BikeStatusForm(forms.ModelForm):
    position = gis_forms.PointField(
        required=False,
        widget=widgets.SmbOsmWidget(
            attrs={
                "default_lon": 12,
                "default_lat": 41,
                "default_zoom": 6,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        bike = kwargs.pop("bike", None)
        is_ajax = kwargs.pop("is_ajax", None)
        action = kwargs.pop("action", None)
        submit_value = _(
            "Report lost bike") if not bike else _("Update bike status")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "statusForm"
        if action is not None:
            self.helper.form_action = action

        if bike is None:  # TODO: show only bikes that are not currently lost
            self.fields["bike"].queryset = models.Bike.objects.filter(
                owner=user)
            self.instance.lost = True
            del self.fields["lost"]
        else:
            current_status = bike.get_current_status()
            self.fields["lost"].initial = current_status.lost
            self.instance.bike = bike
            del self.fields["bike"]

        if is_ajax:
            form_layout = self._get_ajax_layout(
                include_bike_field=bike is None)
        else:
            form_layout = self._get_layout(
                submit_value,
                include_lost_field=bike is not None
            )
        self.helper.layout = form_layout

    class Meta:
        model = models.BikeStatus
        fields = (
            "bike",
            "lost",
            "details",
            "position",
        )

    def _get_ajax_layout(self, include_bike_field=True):
        form_layout = layout.Layout(
            layout.Fieldset(
                None,
                "bike",
                "lost",
                "details",
                "position",
            )
        )
        if not include_bike_field:
            form_layout[0].pop(0)
        return form_layout

    def _get_layout(self, submit_value, include_lost_field=True):
        form_layout = layout.Layout(
            layout.Div(
                layout.Div(
                    layout.Field("bike"),
                    layout.Field("lost"),
                    layout.Field("details"),
                    css_class="col-lg-3"
                ),
                layout.Div(
                    layout.Field("position"),
                    css_class="col-lg-9",
                ),
                css_class="row"
            ),
            bootstrap.FormActions(
                layout.Submit("submit", submit_value)
            ),
        )
        if not include_lost_field:
            form_layout[0][0].pop(1)
        return form_layout


class BikePictureForm(forms.ModelForm):
    image = forms.ImageField(
        label=_("image"),
        widget=forms.ClearableFileInput(
            attrs={
                "data-upload-max-size-megabytes": settings.SMB_PORTAL.get(
                    "max_upload_size_megabytes", 2),
                "data-success-message": _("Upload picture"),
                "data-success-icon-classes": "fa fa-upload",
                "data-error-message": _("Picture too big to upload"),
                "data-error-icon-classes": "fa fa-ban",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.bike = kwargs.pop("bike", None)
        is_ajax = kwargs.pop("is_ajax", None)
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        self.instance.gallery = self.bike.picture_gallery
        self.helper = FormHelper()
        if action is not None:
            self.helper.form_action = action
        self.helper.layout = layout.Layout(
            layout.Field("image"),
        )
        form_id = "bikePictureForm"
        self.helper.form_id = form_id
        if not is_ajax:
            self.helper.layout.append(
                bootstrap.FormActions(
                    bootstrap.StrictButton(
                        mark_safe('<i class="fa fa-upload"></i> ') + _(
                            "Upload picture"),
                        type="submit",
                        form=form_id,
                        css_class="btn btn-primary"
                    ),
                )
            )

    def clean_image(self):
        data = self.cleaned_data.get("image")
        logger.debug("data: {}".format(data))
        if data is not None:
            validators.validate_file_size(data)
        else:
            raise forms.ValidationError(_("could not read uploaded image"))
        return data

    def clean(self):
        """Perform validation of fields that depend on each other

        We are re-implementing this method because the photologue ``Photo``
        model requires a unique ``slug`` field for an uploaded photo. Since
        we chose not to include this field in the upload form, but to
        construct it dynamically instead, we need to validate it before it
        reaches the DB (where it will fail if the slug is not unique)

        """

        super().clean()
        uploaded_image = self.cleaned_data.get("image")
        if uploaded_image is not None:
            file_name = uploaded_image.name
            title = "-".join((str(self.bike.pk), file_name))
            slugged_title = slugify(title)
            gallery = self.bike.picture_gallery
            if gallery.photos.filter(slug=slugged_title).exists():
                # FIXME: should be passing "image" as the ``field`` value here
                #        However, that makes the template render a non-styled
                #        message next to the failing field. By passing ``None``
                #        we are at least rendering a correctly styled error
                #        in the template
                self.add_error(
                    None, _("Already uploaded a picture with that name"))
            else:
                self.instance.title = title

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.title)
        self.instance.caption = "caption for photo {}".format(
            self.instance.title)
        return super().save(commit=commit)

    class Meta:
        model = models.BikePicture
        fields = (
            "image",
            # "caption",
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
                "required": _("Must select at least one picture to delete"),
            }
        )
