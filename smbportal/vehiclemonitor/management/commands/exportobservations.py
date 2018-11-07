#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

import pathlib

from django.core.management.base import BaseCommand

from vehiclemonitor import exporter
from vehiclemonitor import models


def _parse_lookup(value):
    return value.split("=")


class Command(BaseCommand):
    help = "Export observation data to CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "output_path",
        )
        parser.add_argument(
            "-s",
            "--queryset-lookup",
            action="append",
            help="Lookup to use when selecting which observations should be "
                 "exported",
            type=_parse_lookup
        )

    def handle(self, *args, **options):
        observations = models.BikeObservation.objects.all()
        lookups = options.get("queryset_lookup") or []
        for name, value in lookups:
            self.stdout.write(f"{name}: {value}")
            observations = observations.filter(**{name: value})
        output_path = pathlib.Path(
            options["output_path"]).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()
        exporter.export_observations(observations, output_path)
