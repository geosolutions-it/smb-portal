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

from tracks.exporter import export_segments
from tracks.models import Segment
from vehicles.models import Bike
from vehiclemonitor.exporter import export_observations
from vehiclemonitor.models import BikeObservation

from . import forms

logger = logging.getLogger(__name__)


def dashboard_downloads(request):
    segs_prefix = "segments"
    obs_prefix = "observations"
    render_partial = partial(render, request, "dashboard/analyst_index.html")
    observations_form = forms.ObservationDownloadForm(prefix=obs_prefix)
    segments_form = forms.SegmentDownloadForm(prefix=segs_prefix)
    if request.method == "POST":
        if f"{segs_prefix}-submit" in request.POST:
            form = forms.SegmentDownloadForm(request.POST, prefix=segs_prefix)
            if form.is_valid():
                logger.debug("segments form has been submitted")
                # process and return the zipped shapefile
                segments = _get_segments(
                    form.cleaned_data["start_date"],
                    form.cleaned_data["end_date"]
                )
                result = HttpResponse(segments, content_type="application/zip")
                result["Content-Disposition"] = (
                    "attachment; filename=segments.zip")
            else:
                result = render_partial(
                    {
                        "segments_form": form,
                        "observations_form": observations_form
                    }
                )
        elif f"{obs_prefix}-submit" in request.POST:
            form = forms.ObservationDownloadForm(
                request.POST, prefix=obs_prefix)
            if form.is_valid():
                logger.debug("observations form has been submitted")
                # process and return the csv
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
                result = render_partial(
                    {
                        "segments_form": segments_form,
                        "observations_form": form
                    }
                )
        else:
            raise Http404
    else:
        result = render_partial(
            {
                "segments_form": segments_form,
                "observations_form": observations_form,
            }
        )
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
    export_observations(observations_qs, output_path)
    contents = io.BytesIO()
    with output_path.open("rb") as fh:
        contents.write(fh.read())
    shutil.rmtree(str(output_dir))
    contents.seek(0)
    return contents


# TODO: add filters
def _get_segments(start_date: dt.datetime, end_date: dt.datetime):
    output_dir = pathlib.Path(tempfile.mkdtemp())
    output_path = output_dir / "segments.shp"
    segments_qs = Segment.objects.all()
    if start_date is not None:
        segments_qs = segments_qs.filter(start_date__gte=start_date)
    if end_date is not None:
        segments_qs = segments_qs.filter(end_date__lte=end_date)
    export_segments(segments_qs, output_path)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w") as zh:
        for item in output_path.parent.iterdir():
            if item.is_file():
                zh.write(item, arcname=item.name)
    shutil.rmtree(str(output_dir))
    zip_buffer.seek(0)
    return zip_buffer
