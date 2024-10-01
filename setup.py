import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/course-dashboards>`_.
"""


# The VERSION file is created by travis-ci, based on the tag name
version_path = 'coursedashboards/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/course-dashboards"
setup(
    name='coursedashboards',
    version=VERSION,
    packages=['coursedashboards'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django~=4.2',
        'psycopg2',
        'django-compressor==4.4',
        'django-pyscss',
        'django_mobileesp',
        'uw-memcached-clients~=1.0',
        'pytz',
        'lxml~=4.9.1',
        'xmlsec==1.3.13',
        'UW-RestClients-Core~=1.3',
        'UW-RestClients-SWS~=2.4',
        'UW-Restclients-PWS~=2.1',
        'UW-RestClients-GWS~=2.3',
        'UW-RestClients-Django-Utils~=2.3',
        'UW-RestClients-Canvas~=1.2',
        'UW-RestClients-Bookstore~=1.1',
        'UW-Django-SAML2~=1.5',
        'Django-SupportTools~=3.5',
        'djangorestframework~=3.15',
        'Django-Persistent-Message',
        'django-person-client~=1.0',
        'statistics',
    ],
    license='Apache License, Version 2.0',
    description='A Django App for viewing course data',
    long_description=README,
    url=url,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
)
