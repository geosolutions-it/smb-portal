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
import logging
import re
from typing import Dict
from typing import List
import zipfile

import boto3
import psycopg2

logger = logging.getLogger(__name__)

TrackData = namedtuple("TrackData", [])


def handle_track_upload(s3_bucket_name: str, object_key: str, db_params: Dict):
    """Ingest track data into smb database"""
    try:
        track_owner = get_track_owner(object_key)
    except AttributeError:
        raise RuntimeError(
            "Could not determine track owner for object {}".format(object_key))
    else:
        raw_data = retrieve_track_data(s3_bucket_name, object_key)
        parsed_data = parse_track_data(raw_data)
        insert_track(parsed_data, track_owner, **db_params)


def insert_track(track_data: List[TrackData], owner: str, dbname: str,
                 user: str, password: str, host: str="localhost",
                 port: str="5432"):
    """Insert track data into the main database"""
    db_connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    cursor = db_connection.cursor()
    cursor.execute("""INSERT INTO tracks_collectedpoint () VALUES""")
    db_connection.commit()
    cursor.close()
    db_connection.close()


def retrieve_track_data(s3_bucket: str, object_key: str) -> str:
    """Download track data file from S3 and return the data"""
    s3 = boto3.resource("s3")
    obj = s3.Object(s3_bucket, object_key)
    response = obj.get()
    # presumably the data is zipped, we must unzip it
    # TODO: do some integrity checks to the data
    result = ""
    with zipfile.ZipFile(response["Body"]) as zip_handler:
        for member_name in zip_handler.namelist():
            result += zip_handler.read(member_name).decode("utf-8")
    return result


def parse_track_data(raw_track_data: str) -> List[TrackData]:
    result = []
    for line in [li for li in raw_track_data.split("\n") if li != ""]:
        result.append(parse_track_data_line(line))
    return result


def parse_track_data_line(line: str) -> TrackData:
    raise NotImplementedError


def get_track_owner(object_key: str) -> str:
    search_obj = re.search(r"cognito/smb/[\\w-]+/(.*)", object_key)
    return search_obj.group(1)
