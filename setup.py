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
    author="UWIT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'django~=5.2',
        'django-compressor',
        'pyscss@git+https://github.com/kronuz/pyscss.git',  # master branch!
        'django-pyscss>=2.0',
        'django_mobileesp',
        'uw-memcached-clients~=1.0',
        'uw-restclients-core~=1.4',
        'uw-restclients-sws~=2.5',
        'uw-restclients-pws~=2.1',
        'uw-restclients-gws~=2.3',
        'uw-restclients-django-utils~=2.3',
        'uw-restclients-canvas~=1.2',
        'uw-restclients-bookstore~=1.1',
        'uw-django-saml2~=1.8',
        'django-supporttools~=3.6',
        'djangorestframework~=3.15',
        'django-persistent-message~=1.3',
        'django-person-client~=2.1',
        'django-blti~=3.0',
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
