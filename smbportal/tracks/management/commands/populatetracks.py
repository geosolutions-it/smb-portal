#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from glob import iglob
import pathlib
from typing import Dict
from typing import List

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from smbbackend import processor
from smbbackend.calculateindexes import calculate_indexes
from smbbackend.updatebadges import update_badges
from smbbackend.exceptions import NonRecoverableError
import smbbackend.utils

from keycloakauth.keycloakadmin import get_manager
from keycloakauth.utils import create_user
from profiles.models import SmbUser
import profiles.models as pm


class Command(BaseCommand):
    help = "Add test data for tracks and segments"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            help="Username of the user that will own the files. If it does "
                 "not exist, a new user is created with the input username "
                 "and a password of 123456"
        )
        parser.add_argument(
            "file-patterns",
            nargs="+",
            help="wildcard pattern (fnmatch) of the files that will be "
                 "imported. This option may be specified multiple times"
        )
        parser.add_argument(
            "--user-age-group",
            help="Age group for the user. This will only be used if the user "
                 "is created from scratch"
        )
        parser.add_argument(
            "--user-occupation",
            help="Occupation for the user. This will only be used if the user "
                 "is created from scratch"
        )

    def handle(self, *args, **options):
        owner = self.get_user(
            options["username"],
            age=options.get("user-age-group"),
            occupation=options.get("user-occupation"),
        )
        for pattern in options["file-patterns"]:
            for path_name in iglob(pattern, recursive=True):
                self.stdout.write(f"Processing file {path_name}...")
                path = pathlib.Path(path_name)
                if path.is_file():
                    self.ingest_file(path, owner)

    def get_user(self, username: str, password="123456",
                 **profile_kwargs) -> SmbUser:
        try:
            user = SmbUser.objects.get(username=username)
            self.stdout.write(f"Found {username!r} user")
        except SmbUser.DoesNotExist:
            self.stdout.write(f"Creating new {username!r} user...")
            keycloak_manager = get_manager(
                settings.KEYCLOAK["base_url"],
                settings.KEYCLOAK["realm"],
                settings.KEYCLOAK["client_id"],
                settings.KEYCLOAK["admin_username"],
                settings.KEYCLOAK["admin_password"],
            )
            user = create_user(
                username,
                email=username if "@" in username else f"{username}@fake.com",
                password=password,
                group_path="/end_users",
                keycloak_manager=keycloak_manager,
                profile_model=pm.EndUserProfile,
                profile_kwargs=profile_kwargs
            )
        return user

    def ingest_file(self, path: pathlib.Path, owner: SmbUser):
        with path.open() as fh:
            raw_data = fh.read()
        points = processor.parse_point_raw_data(raw_data)
        session_id = processor.get_session_id(points)
        connections["default"].connect()
        connection = connections["default"]
        with connection.cursor() as cursor:
            try:
                segments_data = processor.process_data(
                    points,
                    cursor,
                    **processor.DATA_PROCESSING_PARAMETERS
                )
                self.stdout.write(f"segments_data: {segments_data}")
            except NonRecoverableError as exc:
                self.stdout.write(str(exc))
            else:
                is_valid = processor.is_track_valid(segments_data)
                track_id = processor.save_track(
                    session_id, segments_data, owner.keycloak.UID, cursor)
                smbbackend.utils.update_track_info(track_id, cursor)
                self.stdout.write(f"track: {track_id} - valid: {is_valid}")
                if is_valid:
                    calculate_indexes(track_id, cursor)
                    update_badges(track_id, cursor)
