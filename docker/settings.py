from .base_settings import *

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
    'compressor',
    'coursedashboards',
    'userservice',
    'supporttools',
    'persistent_message',
    'rest_framework.authtoken',
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

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = '/static/'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

COMPRESS_PRECOMPILERS += (
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

if not os.getenv("ENV") == "localdev":
    INSTALLED_APPS += ['rc_django',]
    RESTCLIENTS_DAO_CACHE_CLASS = 'coursedashboards.cache.RestClientsCache'

RESTCLIENTS_DEFAULT_TIMEOUT = 3

SUPPORTTOOLS_PARENT_APP = "CoDa"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_VALIDATION_MODULE = "coursedashboards.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "coursedashboards.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "coursedashboards.authorization.can_proxy_restclient"

# PDS config
AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', '')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME', '')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD', '')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', '')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', '')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '')

DETECT_USER_AGENTS = {
    'is_tablet': False,
    'is_mobile': False,
    'is_desktop': True,
}

CODA_ADMIN_GROUP = 'u_acadev_coda_admins'

DEBUG = True if os.getenv('ENV', 'localdev') == "localdev" else False

CODA_PROFILE = True if os.getenv('CODA_PROFILE', 'FALSE') == "TRUE" else False
