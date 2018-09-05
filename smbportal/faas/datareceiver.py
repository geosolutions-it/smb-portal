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

from . import _constants
from ._constants import VehicleType

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
SegmentInfo = namedtuple("SegmentInfo", [
    "id",
    "vehicle_type",
    "length",
    "duration",
    "speed"
])


def get_db_connection(dbname, user, password, host="localhost", port="5432"):
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )


def handle_track_upload(s3_bucket_name: str, object_key: str, db_connection):
    """Ingest track data into smb database"""
    try:
        track_owner = get_track_owner_uuid(object_key)
    except AttributeError:
        raise RuntimeError(
            "Could not determine track owner for object {}".format(object_key))
    raw_data = retrieve_track_data(s3_bucket_name, object_key)
    parsed_data = parse_track_data(raw_data)
    with db_connection:  # changes are committed when `with` block exits
        with db_connection.cursor() as cursor:
            user_id = get_track_owner_internal_id(track_owner, cursor)
            track_id = insert_track(parsed_data, user_id, cursor)
            insert_collected_points(track_id, parsed_data, cursor)
            insert_segments(track_id, track_owner, cursor)
            segments_info = get_segments_info(track_id, cursor)
            for info in segments_info:
                emissions = calculate_emissions(
                    info.vehicle_type, info.length)
                costs = calculate_costs(
                    info.vehicle_type, info.length, info.duration)
                health = calculate_health(
                    info.vehicle_type, info.duration, info.speed)
                insert_segment_data(info.id, emissions, costs, health, cursor)


def get_aggregated_emissions(track_id):
    pass


def insert_segment_data(segment_id, emissions, costs, health, db_cursor):
    _perform_segment_insert(
        "insert-emission.sql", segment_id, emissions, db_cursor)
    _perform_segment_insert(
        "insert-cost.sql", segment_id, costs, db_cursor)
    _perform_segment_insert(
        "insert-health.sql", segment_id, health, db_cursor)


def get_segments_info(track_id, db_cursor):
    db_cursor.execute(
        _get_query("get-segment-info.sql"),
        {"track_id": track_id}
    )
    result = []
    for row in db_cursor.fetchall():
        segment_id, vehicle_type, length_meters, duration = row
        length_km = length_meters / 1000
        duration_hours = duration.seconds / (60 * 60)
        avg_speed = length_km / duration_hours  # km/h
        result.append(
            SegmentInfo(
                id=segment_id,
                vehicle_type=_constants.VehicleType[vehicle_type],
                length=length_meters,
                duration=duration,
                speed=avg_speed
            )
        )
    return result


def _perform_segment_insert(query_filename, segment_id, query_params: dict,
                            db_cursor):
    all_query_params = query_params.copy()
    all_query_params["segment_id"] = segment_id
    db_cursor.execute(
        _get_query(query_filename),
        all_query_params
    )


# FIXME - Account for emission savings on vehicles other than car
def calculate_emissions(vehicle_type: _constants.VehicleType,
                        segment_length: float) -> dict:
    calculated = {
        "so2": _constants.SO2[vehicle_type] * segment_length,
        "nox": _constants.NOX[vehicle_type] * segment_length,
        "co2": _constants.CO2[vehicle_type] * segment_length,
        "co": _constants.CO[vehicle_type] * segment_length,
        "pm10": _constants.PM10[vehicle_type] * segment_length,
    }
    reference_emissions = {
        "so2": _constants.SO2[VehicleType.car] * segment_length,
        "nox": _constants.NOX[VehicleType.car] * segment_length,
        "co2": _constants.CO2[VehicleType.car] * segment_length,
        "co": _constants.CO[VehicleType.car] * segment_length,
        "pm10": _constants.PM10[VehicleType.car] * segment_length,
    }
    emissions = {
        "so2": 0,
        "so2_saved": 0,
        "nox": 0,
        "nox_saved": 0,
        "co2": 0,
        "co2_saved": 0,
        "co": 0,
        "co_saved": 0,
        "pm10": 0,
        "pm10_saved": 0,
    }
    if vehicle_type in ("foot", "bike"):
        emissions.update({
            "so2_saved": calculated["so2"],
            "nox_saved": calculated["nox"],
            "co2_saved": calculated["co2"],
            "co_saved": calculated["co"],
            "pm10_saved": calculated["pm10"],
        })
    else:
        emissions.update({
            "so2": calculated["so2"],
            "nox": calculated["nox"],
            "co2": calculated["co2"],
            "co": calculated["co"],
            "pm10": calculated["pm10"],
        })
    return emissions


def calculate_costs(vehicle_type, length, duration):
    fuel_cost = _get_fuel_cost(length, vehicle_type)
    time_cost = _get_time_cost(duration)
    depreciation_cost = _get_depreciation_cost(length, vehicle_type)
    operation_cost = _get_operation_cost(length, vehicle_type)
    return {
        "fuel": fuel_cost,
        "time": time_cost,
        "depreciation": depreciation_cost,
        "operation": operation_cost,
        "total": fuel_cost + time_cost + depreciation_cost + operation_cost,
    }


def _get_fuel_cost(length, vehicle_type):
    try:
        volume_spent = length * _constants.FUEL_CONSUMPTION[vehicle_type]
        monetary_cost = volume_spent * _constants.FUEL_PRICE[vehicle_type]
    except KeyError:
        monetary_cost = 0
    return monetary_cost


def _get_time_cost(duration):
    duration_hours = duration.seconds / (60 * 60)
    return duration_hours * _constants.TIME_COST_PER_HOUR_EURO


def _get_depreciation_cost(length, vehicle_type):
    try:
        return length * _constants.DEPRECIATION_COST[vehicle_type]
    except KeyError:
        return 0


def _get_operation_cost(length, vehicle_type):
    try:
        return length * _constants.OPERATION_COST[vehicle_type]
    except KeyError:
        return 0


def calculate_health(vehicle_type, duration, speed):
    return {
        "consumed_calories": _get_consumed_calories(
            speed, duration, vehicle_type),
        # "benefit_index": None  # TODO
    }


def _get_consumed_calories(speed, duration, vehicle_type):
    duration_minutes = duration.seconds / 60
    try:
        steps = _constants.CALORY_CONSUMPTION[vehicle_type]["steps"]
    except KeyError:
        result = 0
    else:
        for step in steps:
            if speed < step["speed"]:
                consumption_per_minute = step["calories"]
                break
        else:
            consumption_per_minute = steps[-1]["calories"]
        result = consumption_per_minute * duration_minutes
    return result


def insert_segments(track_id: str, owner_uuid: str, db_cursor):
    db_cursor.execute(
        _get_query("insert-track-segments.sql"),
        {
            "user_uuid": owner_uuid,
            "track_id": track_id,
        }
    )
    segment_ids = db_cursor.fetchall()
    return [item[0] for item in segment_ids]


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
        vehicle_type = _get_vehicle_type(pt.vehicleMode)
        db_cursor.execute(
            query,
            {
                "vehicle_type": vehicle_type.name,
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
                    int(pt.timeStamp) / 1000,
                    pytz.utc
                ),
            }
        )


def _get_vehicle_type(raw_vehicle_type):
    return {
        "foot": _constants.VehicleType.foot,
        "bike": _constants.VehicleType.bike,
        "bus": _constants.VehicleType.bus,
        "car": _constants.VehicleType.car,
        "moped": _constants.VehicleType.average_motorbike,
    }.get(raw_vehicle_type, _constants.VehicleType.unknown)


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
