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
from django.contrib import messages
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
    permission_required = "vehicles.can_list_own_bikes"

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
        return reverse("bikes:detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        """Instantiate a form object

        We re-implement this method in order to pass the current user as an
        initialization parameter. This is useful for performing validation on
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
    form_class = forms.BikeForm
    template_name_suffix = "_update"
    success_message = "Bike details updated!"

    def get_success_url(self):
        bike = self.get_object()
        return reverse("bikes:detail", kwargs={"pk": bike.pk})

    def get_form_kwargs(self):
        """Instantiate a form object

        We re-implement this method in order to pass the current user as an
        initialization parameter. This is useful for performing validation on
        the form's fields.

        """

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            "user": self.request.user,
        })
        logger.debug("BikeUpdateView form kwargs: {}".format(form_kwargs))
        return form_kwargs


class BikeDetailView(LoginRequiredMixin, DetailView):
    model = models.Bike
    context_object_name = "bike"


class BikeDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Bike
    context_object_name = "bike"
    success_url = reverse_lazy("bikes:list")
    success_message = "Bike deleted!"

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return result


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
        response = super().form_valid(form)
        photo = self.object
        current_bike = models.Bike.objects.get(pk=self.kwargs.get("pk"))
        gallery = current_bike.picture_gallery
        gallery.photos.add(photo)
        return response


class BikePossessionHistoryCreateView(LoginRequiredMixin,
                                      mixins.FormUpdatedMessageMixin,
                                      CreateView):
    model = models.BikePossessionHistory
    form_class = forms.BikePossessionHistoryForm
    template_name_suffix = "_create"
    success_message = "Bike status updated!"

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        if pk is not None:
            result = reverse(
                "bikes:detail",
                kwargs={"pk": self.kwargs.get("pk")}
            )
        else:
            result = reverse("bikes:list")
        return result

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["bike"] = self.get_bike()
        return context_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "bike": self.get_bike(),
            "user": self.request.user,
            "initial": {
                "possession_state": models.BikePossessionHistory.STOLEN,
            }
        })
        return kwargs

    def get_bike(self):
        try:
            bike = models.Bike.objects.get(pk=self.kwargs.get("pk"))
        except models.Bike.DoesNotExist:
            bike = None
        return bike

