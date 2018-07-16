#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings
from django.core.management.base import BaseCommand
import pathlib
import requests
import tarfile


class Command(BaseCommand):
    help = ("Download the geolite2 cities database for enbling geodjango's "
            "geoip2 API")

    def add_arguments(self, parser):
        # TODO: add flag for re-downloading the files
        parser.add_argument(
            "--city-url",
            default="http://geolite.maxmind.com/download/geoip/database/"
                    "GeoLite2-City.tar.gz",
            help="URL of the cities database. Defaults to %(default)s"
        )
        parser.add_argument(
            "--country-url",
            default="http://geolite.maxmind.com/download/geoip/database/"
                    "GeoLite2-Country.tar.gz",
            help="URL of the countries database. Defaults to %(default)s"
        )
        parser.add_argument(
            "-f",
            "--force-download",
            action="store_true",
            help="force re-downloading new geolite2 files even if there are "
                 "already local ones"
        )

    def handle(self, *args, **options):
        cities_target = pathlib.Path(
            settings.GEOIP_PATH,
            getattr(settings, "GEOIP_CITY", "GeoLite2-City.mmdb")
        )
        countries_target = pathlib.Path(
            settings.GEOIP_PATH,
            getattr(settings, "GEOIP_COUNTRY", "GeoLite2-Country.mmdb")
        )
        all_there = cities_target.exists() and countries_target.exists()
        if all_there:
            self.stdout.write(
                "geoip database files are already present locally")
        if options["force_download"]:
            self.stdout.write("(re)downloading geoip database files...")
        if not all_there or options["force_download"]:
            self.prepare_geoip_db(options["city_url"], cities_target)
            self.prepare_geoip_db(options["country_url"], countries_target)
        self.stdout.write("Done!")

    def prepare_geoip_db(self, download_url, target_path):
        download_target = pathlib.Path("{}.tar".format(target_path))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(download_url, stream=True)
        with download_target.open("wb") as fh:
            self.stdout.write("Downloading {}...".format(download_url))
            for chunk in response.iter_content(chunk_size=1024):
                fh.write(chunk)
        with tarfile.open(str(download_target)) as tar:
            for member in tar.getmembers():
                if member.isfile():
                    member.name = member.name.rpartition("/")[-1]
                    self.stdout.write("Extracting {}...".format(member.name))
                    tar.extract(member, str(target_path.parent))
        self.stdout.write("Removing {}...".format(download_target))
        download_target.unlink()
