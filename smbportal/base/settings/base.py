#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

"""Base Django settings for smbportal"""

import os

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
import dj_database_url


def get_environment_variable(var_name, default_value=None):
    value = os.getenv(var_name)
    if value is None:
        if default_value is None:
            error_msg = "Set the {0} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg)
        else:
            value = default_value
    return value


def get_boolean_env_value(environment_value, default_value=None):
    raw_value = get_environment_variable(
        environment_value,
        default_value=default_value
    )
    return True if raw_value.lower() in ("true", "1") else False


def get_list_env_value(environment_value, separator=":", default_value=None):
    raw_value = get_environment_variable(
        environment_value,
        default_value=default_value
    )
    return [item for item in raw_value.split(separator) if item != ""]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environment_variable("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean_env_value("DJANGO_DEBUG", False)

ALLOWED_HOSTS = get_list_env_value(
    "DJANGO_ALLOWED_HOSTS", separator=" ", default_value="*")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "bossoidc",
    "djangooidc",
    "bootstrap4",
    "base",
    "avatar",
    "keycloakauth.apps.KeycloakauthConfig",
    "profiles.apps.ProfilesConfig",
    "vehicles.apps.VehiclesConfig",
    "tracks.apps.TracksConfig",
    "rules.apps.AutodiscoverRulesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

WSGI_APPLICATION = "base.wsgi.application"

DATABASES = {
    "default": dj_database_url.parse(
        get_environment_variable(
            "DJANGO_DATABASE_URL",
            default_value="sqlite:///{}".format(
                os.path.join(BASE_DIR, "db.sqlite3")))
    )
}

AUTH_USER_MODEL = "profiles.SmbUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation."
                 "UserAttributeSimilarityValidator"),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation."
                 "NumericPasswordValidator"),
    },
]

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "bossoidc.backend.OpenIdConnectBackend",
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

LANGUAGES = (
    ("en", _("English")),
    ("it", _("Italian")),
)

# LANGUAGE_CODE = "en-us"
USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_URL = "/openid/openid/KeyCloak"

LOGOUT_URL = "/openid/logout"

END_USERS_GROUP = "end_users"

ANALYSTS_GROUP = "analysts"

PRIZE_MANAGERS_GROUP = "prize_managers"

MEDIA_URL = "MEDIA/ROOT/ASSETS/"

#MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')

KEYCLOAK = {
    "base_url": get_environment_variable(
        "KEYCLOAK_BASE_URL", "http://localhost:8080"),
    "realm": get_environment_variable("KEYCLOAK_REALM"),
    "admin_role": "realm_admin",
    "staff_role": "staff_member",
    "client_id": get_environment_variable("DJANGO_KEYCLOAK_CLIENT_ID"),
    "client_public_uri": get_environment_variable(
        "DJANGO_PUBLIC_URL", "http://localhost:8000"),
    "admin_username": get_environment_variable("KEYCLOAK_ADMIN_USERNAME"),
    "admin_password": get_environment_variable("KEYCLOAK_ADMIN_PASSWORD"),
    "group_mappings": {
        END_USERS_GROUP: "/end_users",
        ANALYSTS_GROUP: "/analysts",
        PRIZE_MANAGERS_GROUP: "/prize_managers",
    }
}

OIDC_PROVIDERS = {
    "KeyCloak": {
        "srv_discovery_url": "{base}/auth/realms/{realm}".format(
            base=KEYCLOAK["base_url"],
            realm=KEYCLOAK["realm"]
        ),
        "behaviour": {
            "response_type": "code",  # for authorization code flow
            "scope": [
                "openid",
                "profile",
                "email",
            ],
        },
        "client_registration": {
            "client_id": KEYCLOAK["client_id"],
            "redirect_uris": [
                "{}/openid/callback/login/".format(
                    KEYCLOAK["client_public_uri"]),
            ],
            "post_logout_redirect_uris": [
                "{}/openid/callback/logout".format(
                    KEYCLOAK["client_public_uri"]),
            ],
        },

    }
}

OIDC_AUTH = {
    "OIDC_ENDPOINT": "{base}/auth/realms/{realm}".format(
        base=KEYCLOAK["base_url"],
        realm=KEYCLOAK["realm"]
    ),
    "OIDC_AUDIENCES": [
        KEYCLOAK["client_id"],
    ],
    "OIDC_RESOLVE_USER_FUNCTION": "bossoidc.backend.get_user_by_id",
    "OIDC_BEARER_TOKEN_EXPIRATION_TIME": 4 * 10,  # 4 minutes
}

UPDATE_USER_DATA = "keycloakauth.oidchooks.update_user_data"

LOAD_USER_ROLES = "keycloakauth.oidchooks.load_user_roles"
