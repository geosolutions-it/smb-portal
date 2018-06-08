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

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from photologue.models import Gallery
from photologue.models import Photo

from base import mixins
from profiles import rules as profiles_rules
from . import models
from . import forms

logger = logging.getLogger(__name__)


class BikeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    context_object_name = "bikes"
    permission_required = "profiles.can_view"

    def get_queryset(self):
        return models.Bike.objects.filter(owner=self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            result = settings.LOGIN_URL
        elif not profiles_rules.has_profile(self.request.user):
            result = reverse("profile:create")
        else:
            raise PermissionDenied()
        return result


class BikeCreateView(LoginRequiredMixin, mixins.FormUpdatedMessageMixin,
                     CreateView):
    model = models.Bike
    form_class = forms.BikeForm
    template_name_suffix = "_create"

    @property
    def success_message(self):
        return "Created bike {!r}".format(self.object.nickname)

    def get_success_url(self):
        return reverse("bikes:update", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        """Instantiate a form object

        We re-implement this method in order to pass the current user as an
        initialization parameter. This is useful for perfoming validation on
        the form's fields.

        """

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            "user": self.request.user,
        })
        return form_kwargs

    def form_valid(self, form):
        """Save a new Bike instance into the DB

        BikePossessionHistory and Gallery objects are also created and
        associated to the new bike instance

        """

        result = super().form_valid(form)
        bike = self.object
        possession_history = models.BikePossessionHistory(
            bike=bike,
            reporter=bike.owner,
        )
        possession_history.save()
        gallery_title = "Picture gallery for bike {}".format(bike.pk)
        picture_gallery = Gallery.objects.create(
            title=gallery_title,
            slug=slugify(gallery_title),
        )
        bike.picture_gallery = picture_gallery
        bike.save()
        return result


class BikeUpdateView(LoginRequiredMixin, mixins.FormUpdatedMessageMixin,
                     UpdateView):
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
    template_name_suffix = "_update"

    @property
    def success_message(self):
        return "bike {!r} updated".format(self.object.nickname)

    def get_success_url(self):
        bike = self.get_object()
        return reverse("bikes:detail", kwargs={"pk": bike.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class BikeDetailView(LoginRequiredMixin, DetailView):
    model = models.Bike
    context_object_name = "bike"


class BikeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Bike
    context_object_name = "bike"
    success_url = reverse_lazy("bikes:list")


class BikePictureUploadView(CreateView):
    model = Photo
    fields = (
        "image",
        "title",
        "slug",
        "caption",
    )
    template_name = "vehicles/bike_picture_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["bike"] = models.Bike.objects.get(
            pk=self.kwargs.get("pk"))
        return context_data

    def form_valid(self, form):
        logger.debug("form stuff: {}".format(form.__dict__))
        logger.debug("cleaned image: {}".format(form.cleaned_data["image"]))
        response = super().form_valid(form)
        photo = self.object
        logger.debug("bike_pk: {}".format(self.kwargs.get("pk")))
        current_bike = models.Bike.objects.get(pk=self.kwargs.get("pk"))
        logger.debug("current_bike: {}".format(current_bike))
        gallery = current_bike.picture_gallery
        logger.debug("gallery: {}".format(gallery))
        gallery.photos.add(photo)
        logger.debug("photo instance: {}".format(photo))
        return response
