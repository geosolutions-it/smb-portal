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
from io import BytesIO
import logging
import re
from typing import Dict
from typing import List
import zipfile

import boto3
import psycopg2

logger = logging.getLogger(__name__)

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
    cursor = db_connection.cursor()
    raw_data = retrieve_track_data(s3_bucket_name, object_key)
    parsed_data = parse_track_data(raw_data)
    internal_user_id = get_track_owner_internal_id(track_owner)
    insert_track(parsed_data, track_owner, cursor)
    db_connection.commit()
    cursor.close()
    db_connection.close()


def insert_track(track_data: List[PointData], owner: str, db_cursor):
    """Insert track data into the main database"""
    db_cursor.execute("""INSERT INTO tracks_track () VALUES""")
    db_cursor.execute("""INSERT INTO tracks_collectedpoint () VALUES""")


def insert_collected_point():
    raise NotImplementedError


def retrieve_track_data(s3_bucket: str, object_key: str) -> str:
    """Download track data file from S3 and return the data"""
    s3 = boto3.resource("s3")
    obj = s3.Object(s3_bucket, object_key)
    response = obj.get()
    input_buffer = BytesIO(response["Body"].read())
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
