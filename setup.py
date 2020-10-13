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
        'Django>=2.1,<2.2',
        'django-compressor==2.2',
        'django-pyscss',
        'django_mobileesp',
        'uw-memcached-clients>=1.0.2,<2.0',
        'pytz',
        'AuthZ-Group>=1.6',
        'UW-RestClients-Core>=1.1.1,<2.0',
        'UW-RestClients-SWS>=2.2.5,<3.0',
        'UW-Restclients-PWS==2.0.2',
        'UW-RestClients-GWS>=2.0.1,<3.0',
        'UW-RestClients-Django-Utils>=2.1.5,<3.0',
        'UW-RestClients-Canvas>=1.1.5,<2.0',
        'UW-Django-SAML2>=1.3.8,<2.0',
        'Django-SupportTools>=3.4,<4.0',
        'djangorestframework==3.11.1',
        'statistics',
        'mysqlclient==1.3.14',
    ],
    license='Apache License, Version 2.0',  # example license
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
        'Programming Language :: Python :: 2.7',
    ],
)
