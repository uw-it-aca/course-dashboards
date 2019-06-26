from .base_settings import *

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += [
    'compressor',
    'rc_django',
    'templatetag_handlebars',
    'coursedashboards',
    'userservice',
    'supporttools'
]

MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
]


COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = '/static/'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

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
RESTCLIENTS_DAO_CACHE_CLASS='coursedashboards.cache.RestClientsCache'
AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.uw_group_service.UWGroupService'
RESTCLIENTS_MEMCACHED_SERVERS = ''

RESTCLIENTS_DEFAULT_TIMEOUT = 3

SUPPORTTOOLS_PARENT_APP = "CoDa"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_OVERRIDE_AUTH_MODULE = "coursedashboards.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "coursedashboards.authorization.can_proxy_restclient"

DETECT_USER_AGENTS = {
    'is_tablet': False,
    'is_mobile': False,
    'is_desktop': True,
}

CODA_ADMIN_GROUP = 'u_acadev_coda_admins'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'appsubmit.cac.washington.edu'

DEBUG = False 
