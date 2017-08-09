This is the repository for the course dashboards project


# Prerequisites

* A Python installation 2.7
* pip or easy_install
* git

# Step-by-step

If you don't have it already, install virtualenv:

```
$ pip install virtualenv
```
if you don't have pip, you may be able to:

```
$ easy_install virtualenv
```
 

Checkout the master of the coursedashboards project:
```
$ git clone git@github.com:uw-it-aca/course-dashboards.git OR https://github.com/uw-it-aca/course-dashboards.git
```

Turn coursedashboards into a virtualenv:
```
$ virtualenv course-dashboards  
```

Activate your virtualenv:
```
cd coursedashboards
source bin/activate
```

Install required Python packages with pip:
```
$ pip install -r requirements.txt
$ pip install uw-restclients
```

If you receive errors with the above, ensure you have lib32z1-dev, libxslt1-dev, libxml2-dev, and python-dev installed. 

Create a django project in the coursedashboards dir:
```
$ django-admin.py startproject project .
```
That '.' at the end is important!

Modify at least the following settings in project/settings.py:
```
    INSTALLED_APPS
    (add: 'compressor', 'templatetag_handlebars', 'coursedashboards.apps.CourseDashboardsConfig', 'restclients', 'userservice')
```


    You need to use MIDDLEWARE_CLASSES instead of MIDDLEWARE.  Add these:
```
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_mobileesp.middleware.UserAgentDetectionMiddleware',
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        'userservice.user.UserServiceMiddleware',
        'restclients.middleware.EnableServiceDegradationMiddleware'
```
    Below that add:
```
     AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.RemoteUserBackend'
     ]
     TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'coursedashboards.context_processors.is_desktop',
                ],
            },
        },
    ]
```
    Add: 
```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# django mobileesp

from django_mobileesp.detector import mobileesp_agent as agent

DETECT_USER_AGENTS = {

    'is_tablet' : agent.detectTierTablet,
    'is_mobile': agent.detectMobileQuick,

    'is_and': agent.detectAndroid,
    'is_ios': agent.detectIos,
    'is_win': agent.detectWindowsPhone,
}

COMPRESS_ROOT = "/tmp/"
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'pyscss {infile} > {outfile}'),
    ('text/x-scss', 'pyscss {infile} > {outfile}'),
)
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
COMPRESS_OUTPUT_DIR = ''
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# htmlmin
HTML_MINIFY = True
```


Add include to your imports in project/urls.py:
```
from django.conf.urls import include, url
from django.contrib import admin
```

Map urls to the coursedashboards app by adding the following to urlpatterns in project/urls.py:
```
urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('coursedashboards.urls')),
]
```

```
$ python manage.py migrate
```

You should now be able to run your development server:
```
$ python manage.py runserver 0.0.0.0:<your port>
```
Run as a mock user e.g., javerage:
```
$ REMOTE_USER=<netid> ./manage.py runserver 0.0.0.0:<your port>
```
