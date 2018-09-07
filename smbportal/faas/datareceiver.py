#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Data receiver utilities"""

# -  whenever data is stored in AWS S3, a new message is pushed to SNS, which
#    asynchronously delivers it to subscribed consumers
# -  some web app exposes an endpoint that is subscribed to the AWS SNS
# -  SNS issues a POST request to the web app's endpoint, sending a message
#    that informs of new data present in S3

from collections import namedtuple
import datetime as dt
import io
import logging
import os
import pathlib
import re
from typing import Dict
from typing import List
import zipfile

import boto3
import psycopg2
import pytz

logger = logging.getLogger(__name__)

_VEHICLE_TYPES = {
    1: "foot",
    2: "bike",
    3: "bus",
}

_DATA_FIELDS = [
    "accelerationX",
    "accelerationY",
    "accelerationZ",
    "accuracy",
    "batConsumptionPerHour",
    "batteryLevel",
    "deviceBearing",
    "devicePitch",
    "deviceRoll",
    "elevation",
    "gps_bearing",
    "humidity",
    "latitude",
    "longitude",
    "lumen",
    "pressure",
    "proximity",
    "sessionId",
    "speed",
    "temperature",
    "timeStamp",
    "vehicleMode",
    "serialVersionUID",

]

PointData = namedtuple("PointData", _DATA_FIELDS)


def handle_track_upload(s3_bucket_name: str, object_key: str, db_params: Dict):
    """Ingest track data into smb database"""
    try:
        track_owner = get_track_owner_uuid(object_key)
    except AttributeError:
        raise RuntimeError(
            "Could not determine track owner for object {}".format(object_key))

    db_connection = psycopg2.connect(
        host=db_params["host"],
        port=db_params["port"],
        dbname=db_params["dbname"],
        user=db_params["user"],
        password=db_params["password"]
    )
    raw_data = retrieve_track_data(s3_bucket_name, object_key)
    parsed_data = parse_track_data(raw_data)
    with db_connection:
        with db_connection.cursor() as cursor:
            user_id = get_track_owner_internal_id(track_owner, cursor)
            track_id = insert_track(parsed_data, user_id, cursor)
            insert_collected_points(track_id, parsed_data, cursor)
            insert_segments(track_id)


def insert_segments(track_id: str, db_cursor):
    for vehicle_type in _VEHICLE_TYPES.values():
        insert_vehicle_type_segments(track_id, vehicle_type, db_cursor)


def insert_vehicle_type_segments(track_id, vehicle_type, db_cursor):
    query = _get_query("create-track-segment.sql")
    db_cursor.execute(
        query,
        {
            "track_id": track_id,
            "vehicle_type": vehicle_type
        }
    )


def insert_track(track_data: List[PointData], owner: str, db_cursor) -> str:
    """Insert track data into the main database"""
    session_id = list(set([pt.sessionId for pt in track_data]))[0]
    query = _get_query("insert-track.sql")
    db_cursor.execute(
        query,
        (owner, session_id, dt.datetime.now(pytz.utc))
    )
    track_id = db_cursor.fetchone()[0]
    return track_id


def insert_collected_points(track_id: str, track_data: List[PointData],
                            db_cursor):
    query = _get_query("insert-collectedpoint.sql")
    for pt in track_data:
        db_cursor.execute(
            query,
            {
                "vehicle_type": _VEHICLE_TYPES[pt.vehicleMode],
                "track_id": track_id,
                "longitude": pt.longitude,
                "latitude": pt.latitude,
                "accelerationx": pt.accelerationX,
                "accelerationy": pt.accelerationY,
                "accelerationz": pt.accelerationZ,
                "accuracy": pt.accuracy,
                "batconsumptionperhour": pt.batConsumptionPerHour,
                "batterylevel": pt.batteryLevel,
                "devicebearing": pt.deviceBearing,
                "devicepitch": pt.devicePitch,
                "deviceroll": pt.deviceRoll,
                "elevation": pt.elevation,
                "gps_bearing": pt.gps_bearing,
                "humidity": pt.humidity,
                "lumen": pt.lumen,
                "pressure": pt.pressure,
                "proximity": pt.proximity,
                "speed": pt.speed,
                "temperature": pt.temperature,
                "sessionid": pt.sessionId,
                "timestamp": dt.datetime.fromtimestamp(
                    pt.timeStamp / 1000,
                    pytz.utc
                ),
            }
        )


def retrieve_track_data(s3_bucket: str, object_key: str) -> str:
    """Download track data file from S3 and return the data"""
    s3 = boto3.resource("s3")
    obj = s3.Object(s3_bucket, object_key)
    response = obj.get()
    input_buffer = io.BytesIO(response["Body"].read())
    # TODO: do some integrity checks to the data
    result = ""
    with zipfile.ZipFile(input_buffer) as zip_handler:
        for member_name in zip_handler.namelist():
            result += zip_handler.read(member_name).decode("utf-8")
    return result


def parse_track_data(raw_track_data: str) -> List[PointData]:
    result = []
    for index, line in enumerate(raw_track_data.splitlines()):
        if index > 0 and line != "":  # ignoring first line, it is file header
            result.append(parse_track_data_line(line))
    return result


def parse_track_data_line(line: str) -> PointData:
    info = line.split(",")
    return PointData(*info[:len(_DATA_FIELDS)])


def get_track_owner_uuid(object_key: str) -> str:
    search_obj = re.search(r"cognito/smb/([\w-]{36})", object_key)
    return search_obj.group(1)


def get_track_owner_internal_id(keycloak_uuid: str, db_cursor):
    db_cursor.execute(
        "SELECT user_id FROM bossoidc_keycloak WHERE \"UID\" = %s",
        (keycloak_uuid,)
    )
    return db_cursor.fetchone()[0]


def _get_query(filename) -> str:
    base_dir = pathlib.Path(os.path.abspath(__file__)).parent
    query_path = base_dir / "sqlqueries" / filename
    with query_path.open(encoding="utf-8") as fh:
        query = fh.read()
    return query
