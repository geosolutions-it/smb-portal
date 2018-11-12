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

from dashboard import exporter
from vehicles import models


def _parse_lookup(value):
    return value.split("=")


class Command(BaseCommand):
    help = "Export status history data to csv"

    def add_arguments(self, parser):
        parser.add_argument(
            "output_path",
        )
        parser.add_argument(
            "-s",
            "--queryset-lookup",
            action="append",
            help="Lookup to use when selecting which bike statuses should be "
                 "exported",
            type=_parse_lookup
        )

    def handle(self, *args, **options):
        bike_statuses = models.BikeStatus.objects.all()
        lookups = options.get("queryset_lookup") or []
        for name, value in lookups:
            self.stdout.write(f"{name}: {value}")
            bike_statuses = bike_statuses.filter(**{name: value})
        output_path = pathlib.Path(
            options["output_path"]).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()
        exporter.export_bike_statuses(bike_statuses, output_path)
