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
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
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

        BikeStatus and Gallery objects are also created and associated with
        the new bike instance

        """

        result = super().form_valid(form)
        bike = self.object
        bike_status = models.BikeStatus(
            bike=bike,
            reporter=bike.owner,
            lost=False
        )
        bike_status.save()
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


class BikeGalleryDetailView(LoginRequiredMixin, DetailView):
    model = Gallery
    context_object_name = "gallery"
    template_name = "vehicles/bikegallery_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["bike"] = _get_current_bike(self.kwargs)
        return context_data

    def get_object(self, queryset=None):
        bike = _get_current_bike(self.kwargs)
        return bike.picture_gallery


class BikePictureUploadView(LoginRequiredMixin,
                            mixins.FormUpdatedMessageMixin,
                            CreateView):
    model = Photo
    form_class = forms.BikePictureForm
    template_name = "vehicles/bike_picture_create.html"
    success_message = "Bike picture uploaded!"

    def get_success_url(self):
        bike = _get_current_bike(self.kwargs)
        return reverse("bikes:gallery", kwargs={"pk": bike.pk})

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["bike"] = _get_current_bike(self.kwargs)
        return context_data

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            "bike": _get_current_bike(self.kwargs),
        })
        return form_kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        photo = self.object
        current_bike = _get_current_bike(self.kwargs)
        gallery = current_bike.picture_gallery
        gallery.photos.add(photo)
        return response


class BikePictureDeleteView(LoginRequiredMixin, View):
    form_class = forms.BikePictureDeleteForm
    template_name = "vehicles/bike_picture_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        return render(
            request,
            self.template_name,
            context=self.get_context_data(form=form)
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, **self.get_form_kwargs())
        if form.is_valid():
            for picture_id in form.cleaned_data["choices"]:
                picture = Photo.objects.get(pk=picture_id)
                picture.delete()
            messages.success(request, "Pictures have been deleted!")
            bike = _get_current_bike(kwargs)
            result = redirect("bikes:gallery", pk=bike.pk)
        else:
            result = render(
                request,
                self.template_name,
                context=self.get_context_data(form=form)
            )
        return result

    def get_context_data(self, **kwargs):
        context_data = kwargs.copy()
        context_data["bike"] = _get_current_bike(self.kwargs)
        return context_data

    def get_form_kwargs(self):
        return {
            "bike": _get_current_bike(self.kwargs),
        }


class BikeStatusCreateView(LoginRequiredMixin,
                           mixins.FormUpdatedMessageMixin,
                           CreateView):
    model = models.BikeStatus
    form_class = forms.BikeStatusForm
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
        context_data["bike"] = _get_current_bike(self.kwargs)
        return context_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "bike": _get_current_bike(self.kwargs),
            "user": self.request.user,
            "initial": {
                "lost": True,
            }
        })
        return kwargs

    def get_bike(self):
        try:
            bike = models.Bike.objects.get(pk=self.kwargs.get("pk"))
        except models.Bike.DoesNotExist:
            bike = None
        return bike


def _get_current_bike(view_kwargs):
    try:
        bike = models.Bike.objects.get(pk=view_kwargs.get("pk"))
    except models.Bike.DoesNotExist:
        bike = None
    return bike
