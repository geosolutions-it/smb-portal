########################################################################
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
import pathlib

from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as message_constants
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


BASE_DIR = str(pathlib.Path(os.path.abspath(__file__)).parents[2])


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_environment_variable("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean_env_value("DJANGO_DEBUG", "false")

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
    "django.contrib.sites",
    "django.forms",
    "rest_framework",
    "rest_framework_gis",
    "django_filters",
    "drf_yasg",
    "bossoidc",
    "djangooidc",
    "crispy_forms",
    "photologue",
    "sortedm2m",
    "django_bootstrap_breadcrumbs",
    "avatar",
    "base.apps.BaseConfig",
    "keycloakauth.apps.KeycloakauthConfig",
    "profiles.apps.ProfilesConfig",
    "vehicles.apps.VehiclesConfig",
    "tracks.apps.TracksConfig",
    "vehiclemonitor.apps.VehiclemonitorConfig",
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
    "base.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "base.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ]
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

WSGI_APPLICATION = "base.wsgi.application"

DATABASES = {
    "default": dj_database_url.parse(
        get_environment_variable(
            "DJANGO_DATABASE_URL",
            default_value="sqlite:///{}".format(
                os.path.join(BASE_DIR, "db.sqlite3")))
    )
}

SITE_ID = 1

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

LANGUAGE_CODE = "it"

TIME_ZONE = "UTC"

USE_I18N = True

GEOIP_PATH = get_environment_variable(
    "DJANGO_GEOIP_PATH",
    default_value=str(pathlib.Path(BASE_DIR).parent / "GeoLite2"),
)

IPWARE = {
    "proxy_count": 1,
}

LANGUAGES = (
    ("en", _("English")),
    ("it", _("Italian")),
)

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = get_environment_variable(
    "DJANGO_STATIC_ROOT",
    default_value=str(pathlib.Path(BASE_DIR).parent / "static_root"),
)
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

EMAIL_HOST = get_environment_variable(
    "DJANGO_EMAIL_HOST", "smtp.geo-solutions.it")
EMAIL_USE_SSL = get_boolean_env_value("DJANGO_EMAIL_USE_SSL", "false")
EMAIL_PORT = int(get_environment_variable("DJANGO_EMAIL_PORT", "587"))
EMAIL_HOST_USER = get_environment_variable("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_environment_variable("DJANGO_EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

BREADCRUMBS_TEMPLATE = "base/breadcrumbs.html"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "oidc_auth.authentication.BearerTokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "keycloakauth.permissions.DjangoRulesPermission",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"),
    "PAGE_SIZE": 20,
}

AVATAR_AUTO_GENERATE_SIZES = (
    80,
    150,
)

CRISPY_TEMPLATE_PACK = "bootstrap4"

MESSAGE_TAGS = {
    message_constants.DEBUG: "alert-info",
    message_constants.INFO: "alert-info",
    message_constants.SUCCESS: "alert-success",
    message_constants.WARNING: "alert-warning",
    message_constants.ERROR: "alert-error",
}

LOGIN_URL = "/openid/openid/KeyCloak"

LOGOUT_URL = "/openid/logout"

END_USER_PROFILE = "end_users"

ANALYST_PROFILE = "analysts"

PRIZE_MANAGER_PROFILE = "prize_managers"

PRIVILEGED_USER_PROFILE = "privileged_users"

MEDIA_URL = "/media/"

MEDIA_ROOT = get_environment_variable(
    "DJANGO_MEDIA_ROOT",
    default_value=str(pathlib.Path(BASE_DIR).parent / "media"),
)

KEYCLOAK = {
    "base_url": get_environment_variable(
        "KEYCLOAK_BASE_URL", "http://localhost:8080"),
    "realm": get_environment_variable("KEYCLOAK_REALM"),
    "admin_role": "portal_admin",
    "staff_role": "portal_staff",
    "client_id": get_environment_variable("DJANGO_KEYCLOAK_CLIENT_ID"),
    "client_public_uri": get_environment_variable(
        "DJANGO_PUBLIC_URL", "http://localhost:8000"),
    "admin_username": get_environment_variable("KEYCLOAK_ADMIN_USERNAME"),
    "admin_password": get_environment_variable("KEYCLOAK_ADMIN_PASSWORD"),
    "group_mappings": {
        END_USER_PROFILE: [
            "/end_users",
        ],
        ANALYST_PROFILE: [
            "/analysts",
        ],
        PRIZE_MANAGER_PROFILE: [
            "/prize_managers",
        ],
        PRIVILEGED_USER_PROFILE: [
            "/privileged_users"
        ]
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
    "OIDC_BEARER_TOKEN_EXPIRATION_TIME": 4 * 60,  # 4 minutes
}

UPDATE_USER_DATA = "keycloakauth.oidchooks.update_user_data"

LOAD_USER_ROLES = "keycloakauth.oidchooks.load_user_roles"

SMB_PORTAL = {
    "max_upload_size_megabytes": 2,
    "max_bikes_per_user": 5,
    "max_pictures_per_bike": 5,
    "num_latest_observations": 5,
}
