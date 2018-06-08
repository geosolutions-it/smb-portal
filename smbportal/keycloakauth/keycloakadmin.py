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

import logging

import requests

logger = logging.getLogger(__name__)


class KeycloakManager(object):

    def __init__(self, base_url, realm, admin_username, admin_password):
        self.base_url = base_url
        self.realm = realm
        access_token = self.get_access_token(admin_username, admin_password)
        self.access_token = access_token.get("access_token")
        self.refresh_token = access_token.get("refresh_token")

    @property
    def headers(self):
        return {
            "Authorization": "bearer {}".format(self.access_token)
        }

    def get_access_token(self, admin_username, admin_password):
        token_response = requests.post(
            "{}/auth/realms/master/protocol/openid-connect/token".format(
                self.base_url),
            data={
                "client_id": "admin-cli",
                "grant_type": "password",
                "username": admin_username,
                "password": admin_password,
            },
        )
        token_response.raise_for_status()
        return token_response.json()

    def refresh_access_token(self):
        logger.debug("refreshing access_token...")
        token_response = requests.post(
            "{}/auth/realms/master/protocol/openid-connect/token".format(
                self.base_url),
            data={
                "client_id": "admin-cli",
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            },
        )
        token_response.raise_for_status()
        new_access_token = token_response.json()["access_token"]
        self.access_token = new_access_token

    def get_groups(self):
        """Get representation of groups associated with the keycloak realm"""
        groups_response = self._make_request(
            requests.get,
            url="{base}/auth/admin/realms/{realm}/groups".format(
                base=self.base_url,
                realm=self.realm,
            ),
            headers=self.headers
        )
        return groups_response.json()

    def set_user_access(self, user_id: str, enabled: bool=True) -> int:
        return self.set_user_properties(user_id, enabled=enabled)

    def set_user_properties(self, user_id, **user_properties) -> int:
        headers = self.headers.copy()
        headers.update({
            "Content-Type": "application/json",
        })
        response = self._make_request(
            requests.put,
            url="{base}/auth/admin/realms/{realm}/users/{id}".format(
                base=self.base_url,
                realm=self.realm,
                id=user_id
            ),
            json=user_properties,
            headers=headers
        )
        return response.status_code

    def get_user_details(self, username):
        users_response = self._make_request(
            requests.get,
            url="{base}/auth/admin/realms/{realm}/users".format(
                base=self.base_url,
                realm=self.realm,
            ),
            params={
                "username": username,
            },
            headers=self.headers
        )
        user = users_response.json()[0]
        id_ = user["id"]
        user_details = self.get_user_by_id(id_)
        user_details["groups"] = self.get_user_groups(id_)
        return user_details

    def get_user_by_id(self, user_id):
        user_details = self._make_request(
            requests.get,
            url="{base}/auth/admin/realms/{realm}/users/{id}".format(
                base=self.base_url,
                realm=self.realm,
                id=user_id,
            ),
            headers=self.headers
        )
        return user_details.json()

    def get_user_groups(self, user_id):
        response = self._make_request(
            requests.get,
            url="{base}/auth/admin/realms/{realm}/users/{id}/groups".format(
                base=self.base_url,
                realm=self.realm,
                id=user_id,
            ),
            headers=self.headers
        )
        return response.json()

    def add_user_to_group(self, user_id: str, group_path: str):
        """Add an existing keycloak user to an existing keycloak group"""
        groups = self.get_groups()
        group_id = [g["id"] for g in groups if g["path"] == group_path][0]
        response = requests.put(
            "{base}/auth/admin/realms/{realm}/users/{uid}/groups/{gid}".format(
                base=self.base_url,
                realm=self.realm,
                uid=user_id,
                gid=group_id,
            ),
            headers=self.headers
        )
        response.raise_for_status()

    def _make_request(self, request_handler, **request_kwargs):
        handler_kwargs = request_kwargs.copy()
        response = request_handler(**handler_kwargs)
        if response.status_code == 401:  # unauthorized
            self.refresh_access_token()
            handler_kwargs["headers"]["Authorization"] = "bearer {}".format(
                self.access_token)
            response = request_handler(**handler_kwargs)
            response.raise_for_status()
        return response
