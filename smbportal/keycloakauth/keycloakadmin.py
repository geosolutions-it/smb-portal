#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Utilities to communicate with a KeyCloak server using its REST API"""

import datetime as dt
import json
import logging

import requests
from jwkest.jwt import JWT

logger = logging.getLogger(__name__)

_REQUEST_HANDLERS = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put,
    "delete": requests.delete,
}


def get_manager(base_url: str, realm: str, client_id: str, username: str,
                password: str) -> "KeycloakManager":
    # - try to connect to keycloak assuming user exists inside the realm
    # - if that fails, try to connect assuming the user exists in the `master`
    #   realm. In this second case, update the `client_id` too
    client = KeycloakApiClient(base_url, realm, client_id)
    logger.debug("created client. Now to try and obtain token...")
    try:
        client.init_tokens(username, password)
    except requests.HTTPError:
        logger.warning("Could not acquire access token for user. Trying to "
                       "connect to the `master` realm instead...")
        client.realm = "master"
        client.client_id = "admin-cli"
        client.well_known_config = client.get_api_endpoints()
        client.init_tokens(username, password)
        logger.debug("setting client realm back to the original value...")
        client.realm = realm
    manager = KeycloakManager(client)
    return manager


def get_token_password(token_url, client_id, username, password):
    return _get_token(
        token_url,
        client_id,
        grant_type="password",
        username=username,
        password=password
    )


def refresh_access_token(token_url, client_id, refresh_token):
    return _get_token(
        token_url,
        client_id,
        grant_type="refresh_token",
        refresh_token=refresh_token
    )


def get_user_info(userinfo_url, access_token):
    response = _make_auth_request(
        userinfo_url,
        headers={
            "Authorization": "bearer {}".format(access_token)
        }
    )
    return response.json()


class KeycloakApiClient(object):
    well_known_url_pattern = (
        "{base_url}/auth/realms/{realm}/.well-known/openid-configuration")
    access_token_expires_at = None
    refresh_token_expires_at = None
    _access_token = None
    _refresh_token = None
    _user_info = None

    def __init__(self, base_url, realm, client_id,
                 username=None, password=None):
        self.base_url = base_url
        self.realm = realm
        self.client_id = client_id
        self.well_known_config = self.get_api_endpoints()
        if username and password:
            self.init_tokens(username, password)

    @property
    def well_known_configuration_endpoint(self):
        return self.well_known_url_pattern.format(
            base_url=self.base_url, realm=self.realm)

    @property
    def authorization_header(self):
        return "bearer {}".format(self.access_token)

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def user_info(self):
        if self.access_token is None:
            result = None
        elif self._user_info is None:
            self._user_info = get_user_info(
                self.well_known_config["userinfo_endpoint"],
                self.access_token
            )
            result = self._user_info
        else:
            result = None
        return result

    @property
    def is_access_token_expired(self):
        return dt.datetime.utcnow() > self.access_token_expires_at

    @property
    def unpacked_access_token(self):
        return JWT().unpack(self.access_token).payload()

    @property
    def unpacked_refresh_token(self):
        return JWT().unpack(self.refresh_token).payload()

    def get_api_endpoints(self):
        response = _do_request(
            url=self.well_known_configuration_endpoint
        )
        return response.json()

    def init_tokens(self, username, password):
        token_endpoint = self.well_known_config["token_endpoint"]
        token = get_token_password(
            token_endpoint, self.client_id, username, password)
        self._set_tokens(token)

    def _set_tokens(self, token_json_response):
        now = dt.datetime.utcnow()
        self.access_token_expires_at = now + dt.timedelta(
            seconds=token_json_response["expires_in"])
        self.refresh_token_expires_at = now + dt.timedelta(
            seconds=token_json_response["refresh_expires_in"])
        self._access_token = token_json_response["access_token"]
        self._refresh_token = token_json_response["refresh_token"]

    def refresh_access_token(self):
        logger.debug("refreshing access_token...")
        token_endpoint = self.well_known_config["token_endpoint"]
        token_json = refresh_access_token(
            token_endpoint, self.client_id, self.refresh_token)
        self._set_tokens(token_json)

    def make_request(self, api_endpoint, http_method="get", **kwargs):
        url = "{base_url}/auth/admin/realms/{realm}/{end}".format(
            base_url=self.base_url,
            realm=self.realm,
            end=api_endpoint[1:] if api_endpoint[0] == "/" else api_endpoint
        )
        request_kwargs = kwargs.copy()
        headers = {
            "Authorization": self.authorization_header
        }
        headers.update(request_kwargs.pop("headers", {}))
        request_kwargs["headers"] = headers
        response = _do_request(url, http_method, **request_kwargs)
        if response.status_code == 401:  # unauthorized
            self.refresh_access_token()
            request_kwargs[
                "headers"]["Authorization"] = self.authorization_header
            response = _do_request(url, http_method, **request_kwargs)
        response.raise_for_status()
        return response


class KeycloakManager(object):

    def __init__(self, keycloak_api_client):
        self.keycloak_client = keycloak_api_client

    @property
    def user_info(self):
        return self.keycloak_client.user_info

    @property
    def access_token(self):
        return self.keycloak_client.access_token

    @property
    def unpacked_access_token(self):
        return self.keycloak_client.unpacked_access_token

    def create_user(self, username, email=None, password=None, first_name=None,
                    last_name=None, enabled=True, **kwargs):
        payload = {
            "username": username,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "enabled": enabled,
        }
        if password is not None:
            payload["credentials"] = [{
                "type": "password",
                "value": password
            }]
        payload.update(kwargs)
        cleaned_payload = {k: v for k, v in payload.items() if v is not None}
        response = self.keycloak_client.make_request(
            "/users",
            "post",
            data=json.dumps(cleaned_payload),
            headers={
                "Content-Type": "application/json"
            }
        )

    def delete_user(self, user_id):
        self.keycloak_client.make_request(
            "/users/{id}".format(id=user_id),
            http_method="delete"
        )


    def get_groups(self):
        """Get representation of groups associated with the keycloak realm"""
        response = self.keycloak_client.make_request(
            "/groups"
        )
        return response.json()

    def set_user_access(self, user_id: str, enabled: bool=True) -> int:
        return self.set_user_properties(user_id, enabled=enabled)

    def set_user_properties(self, user_id, **user_properties) -> int:
        response = self.keycloak_client.make_request(
            "/users/{id}".format(id=user_id),
            http_method="put",
            json=user_properties,
            headers={
                "Content-Type": "application/json"
            }
        )
        return response.status_code

    def get_user_by_id(self, user_id):
        response = self.keycloak_client.make_request(
            "/users/{id}".format(id=user_id)
        )
        return response.json()

    def get_user_details(self, username):
        users_response = self.keycloak_client.make_request(
            "/users",
            params={
                "username": username
            }
        )
        user = users_response.json()[0]
        id_ = user["id"]
        user_details = self.get_user_by_id(id_)
        user_details["groups"] = self.get_user_groups(id_)
        return user_details

    def get_user_groups(self, user_id):
        response = self.keycloak_client.make_request(
            "/users/{id}/groups".format(id=user_id))
        return response.json()

    def add_user_to_group(self, user_id: str, group_path: str):
        """Add an existing keycloak user to an existing keycloak group"""
        groups = self.get_groups()
        group_id = [g["id"] for g in groups if g["path"] == group_path][0]
        response = self.keycloak_client.make_request(
            "/users/{uid}/groups/{gid}".format(uid=user_id, gid=group_id),
            http_method="put",
        )
        return response.status_code


def _get_token(token_endpoint, client_id, grant_type, **data_kwargs):
    request_data = {
        "client_id": client_id,
        "grant_type": grant_type,
    }
    request_data.update(data_kwargs)
    response = _make_auth_request(
        url=token_endpoint,
        http_method="post",
        data=request_data
    )
    return response.json()


def _make_auth_request(url, http_method="get", **kwargs):
    handler = _REQUEST_HANDLERS.get(http_method.lower())
    response = handler(url=url, **kwargs)
    response.raise_for_status()
    return response


def _do_request(url, http_method="get", **kwargs):
    request_kwargs = kwargs.copy()
    request_handler = _REQUEST_HANDLERS.get(http_method.lower())
    return request_handler(url=url, **request_kwargs)
