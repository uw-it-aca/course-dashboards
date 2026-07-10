from .base_settings import *
import os

ALLOWED_HOSTS = ['*']

if os.getenv('AUTH', 'NONE') == 'SAML_MOCK':
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['bill'],
        'affiliations': ['employee', 'member'],
        'eppn': ['bill@washington.edu'],
        'scopedAffiliations': ['employee@washington.edu', 'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_test_another_group',
                       'u_acadev_coda_admins'],
    }

INSTALLED_APPS += [
    'coursedashboards.apps.CoursedashboardsConfig',
    'uw_person_client',
    'userservice',
    'supporttools',
    'persistent_message',
    'rest_framework.authtoken',
    'django.contrib.postgres',
    'compressor',
]

MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
]

TEMPLATES[0]['DIRS'] = ['/app/coursedashboards/templates/']
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',
]

COMPRESS_OFFLINE = True
COMPRESS_ROOT = '/static/'

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'pyscss {infile} > {outfile}'),
    ('text/x-scss', 'pyscss {infile} > {outfile}'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

USERSERVICE_VALIDATION_MODULE = "coursedashboards.userservice_validation.validate"
USERSERVICE_ADMIN_GROUP='u_acadev_coda_admins'
RESTCLIENTS_ADMIN_GROUP='u_acadev_coda_admins'
PERSISTENT_MESSAGE_AUTH_MODULE = 'coursedashboards.authorization.can_manage_persistent_messages'

if os.getenv("ENV") == "localdev":
    DEBUG = True
    RESTCLIENTS_DAO_CACHE_CLASS = None

    MIGRATION_MODULES = {
        'uw_person_client': 'uw_person_client.test_migrations',
    }
    FIXTURE_DIRS = (
        os.path.join(BASE_DIR, 'uw_person_client', 'fixtures'),
        os.path.join(BASE_DIR, 'coursedashboards', 'fixtures', 'uw_person'),
        os.path.join(BASE_DIR, 'coursedashboards', 'fixtures', 'initial_data'),
    )
else:
    Debug = False
    INSTALLED_APPS += ['rc_django',]
    RESTCLIENTS_DAO_CACHE_CLASS = 'coursedashboards.cache.RestClientsCache'
    RESTCLIENTS_BOOK_HOST = 'https://api.ubookstore.com'
    STORAGES = {
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

RESTCLIENTS_DEFAULT_TIMEOUT = 3

SUPPORTTOOLS_PARENT_APP = "CoDa"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_VALIDATION_MODULE = "coursedashboards.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "coursedashboards.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "coursedashboards.authorization.can_proxy_restclient"

# PDS config, default values are for localdev
DATABASES['uw_person'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': os.getenv('UW_PERSON_DB_HOST', 'postgres'),
    'PORT': os.getenv('UW_PERSON_DB_PORT', '5432'),
    'NAME': os.getenv('UW_PERSON_DB_NAME', 'postgres'),
    'USER': os.getenv('UW_PERSON_DB_USER', 'postgres'),
    'PASSWORD': os.getenv('UW_PERSON_DB_PASSWORD', 'postgres'),
}

DATABASE_ROUTERS = ['uw_person_client.routers.UWPersonRouter']

TZINFOS = {"PDT": -7 * 3600}

DETECT_USER_AGENTS = {
    'is_tablet': False,
    'is_mobile': False,
    'is_desktop': True,
}

CODA_ADMIN_GROUP = 'u_acadev_coda_admins'

CODA_PROFILE = True if os.getenv('CODA_PROFILE', 'FALSE') == "TRUE" else False
