#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import datetime as dt
from functools import partial
import io
import pathlib
import logging
import shutil
import tempfile
from typing import List
from typing import Optional
import zipfile


from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse

from dashboard import exporter
from prizes.models import Winner
from tracks.models import Segment
from vehicles.models import Bike
from vehicles.models import BikeStatus
from vehiclemonitor.models import BikeObservation

from . import forms

logger = logging.getLogger(__name__)


def dashboard_downloads(request):
    observations_form = forms.ObservationDownloadForm(prefix="observations")
    segments_form = forms.SegmentDownloadForm(prefix="segments")
    statuses_form = forms.BikeStatusDownloadForm(prefix="statuses")
    winners_form = forms.CompetitionWinnerDownloadForm(prefix="winners")
    render_partial = partial(render, request, "dashboard/analyst_index.html")
    render_context = {
        "segments_form": segments_form,
        "observations_form": observations_form,
        "statuses_form": statuses_form,
        "winners_form": winners_form,
    }
    if request.method == "POST":
        if f"{segments_form.prefix}-submit" in request.POST:
            form = forms.SegmentDownloadForm(
                request.POST, prefix=segments_form.prefix)
            if form.is_valid():
                segments = _get_segments(
                    form.cleaned_data["start_date"],
                    form.cleaned_data["end_date"]
                )
                result = HttpResponse(segments, content_type="application/zip")
                result["Content-Disposition"] = (
                    "attachment; filename=segments.zip")
            else:
                render_context[segments_form] = form
                result = render_partial(render_context)
        elif f"{observations_form.prefix}-submit" in request.POST:
            form = forms.ObservationDownloadForm(
                request.POST, prefix=observations_form.prefix)
            if form.is_valid():
                observations = _get_observations(
                    form.cleaned_data["start_date"],
                    form.cleaned_data["end_date"],
                    form.cleaned_data["bikes"]
                )
                result = HttpResponse(
                    observations, content_type="text/csv")
                result["Content-Disposition"] = (
                    "attachment; filename=observations.csv")
            else:
                logger.debug(f"form did not validate: {form.errors}")
                render_context["observations_form"] = form
                result = render_partial(render_context)
        elif f"{statuses_form.prefix}-submit" in request.POST:
            form = forms.BikeStatusDownloadForm(
                request.POST, prefix=statuses_form.prefix)
            if form.is_valid():
                statuses = _get_bike_statuses(
                    form.cleaned_data["start_date"],
                    form.cleaned_data["end_date"],
                    form.cleaned_data["bikes"]
                )
                result = HttpResponse(statuses, content_type="text/csv")
                result["Content-Disposition"] = (
                    "attachment; filename=bike_status_history.csv")
            else:
                logger.debug(f"form did not validate: {form.errors}")
                render_context["statuses_form"] = form
                result = render_partial(render_context)
        elif f"{winners_form.prefix}-submit" in request.POST:
            form = forms.CompetitionWinnerDownloadForm(
                request.POST, prefix=winners_form.prefix)
            if form.is_valid():
                statuses = _get_winners(
                    form.cleaned_data["start_date"],
                    form.cleaned_data["end_date"],
                )
                result = HttpResponse(statuses, content_type="text/csv")
                result["Content-Disposition"] = (
                    "attachment; filename=competition_winners.csv")
            else:
                logger.debug(f"form did not validate: {form.errors}")
                render_context["winners_form"] = form
                result = render_partial(render_context)
        else:
            raise Http404
    else:
        result = render_partial(render_context)
    return result


def _get_observations(start_date: Optional[dt.datetime],
                      end_date: Optional[dt.datetime], bikes: List[Bike]):
    output_dir = pathlib.Path(tempfile.mkdtemp())
    output_path = output_dir / "observations.csv"
    observations_qs = BikeObservation.objects.all()
    if start_date is not None:
        observations_qs = observations_qs.filter(observed_at__gte=start_date)
    if end_date is not None:
        observations_qs = observations_qs.filter(observed_at__lte=end_date)
    if len(bikes) != 0:
        observations_qs = observations_qs.filter(bike__in=bikes)
    exporter.export_observations(observations_qs, output_path)
    contents = io.BytesIO()
    with output_path.open("rb") as fh:
        contents.write(fh.read())
    shutil.rmtree(str(output_dir))
    contents.seek(0)
    return contents


def _get_segments(start_date: dt.datetime, end_date: dt.datetime):
    output_dir = pathlib.Path(tempfile.mkdtemp())
    output_path = output_dir / "segments.shp"
    segments_qs = Segment.objects.all()
    if start_date is not None:
        segments_qs = segments_qs.filter(start_date__gte=start_date)
    if end_date is not None:
        segments_qs = segments_qs.filter(end_date__lte=end_date)
    exporter.export_segments(segments_qs, output_path)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w") as zh:
        for item in output_path.parent.iterdir():
            if item.is_file():
                zh.write(item, arcname=item.name)
    shutil.rmtree(str(output_dir))
    zip_buffer.seek(0)
    return zip_buffer


def _get_bike_statuses(start_date: Optional[dt.datetime],
                       end_date: Optional[dt.datetime], bikes: List[Bike]):
    output_dir = pathlib.Path(tempfile.mkdtemp())
    output_path = output_dir / "statuses.csv"
    statuses_qs = BikeStatus.objects.all()
    if start_date is not None:
        statuses_qs = statuses_qs.filter(creation_date__gte=start_date)
    if end_date is not None:
        statuses_qs = statuses_qs.filter(creation_date__lte=end_date)
    if len(bikes) != 0:
        statuses_qs = statuses_qs.filter(bike__in=bikes)
        statuses_qs.order_by("bike")
    exporter.export_bike_statuses(statuses_qs, output_path)
    contents = io.BytesIO()
    with output_path.open("rb") as fh:
        contents.write(fh.read())
    shutil.rmtree(str(output_dir))
    contents.seek(0)
    return contents


def _get_winners(start_date: dt.datetime, end_date: dt.datetime):
    output_dir = pathlib.Path(tempfile.mkdtemp())
    output_path = output_dir / "winners.csv"
    winners_qs = Winner.objects.all()
    if start_date is not None:
        winners_qs = winners_qs.filter(start_date__gte=start_date)
    if end_date is not None:
        winners_qs = winners_qs.filter(end_date__lte=end_date)
    exporter.export_competition_winners(winners_qs, output_path)
    contents = io.BytesIO()
    with output_path.open("rb") as fh:
        contents.write(fh.read())
    shutil.rmtree(str(output_dir))
    contents.seek(0)
    return contents
