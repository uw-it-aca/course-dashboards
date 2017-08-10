import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='coursedashboards',
    version='0.1',
    packages=['coursedashboards'],
    include_package_data=True,
    install_requires=[
        'Django<1.11',
        'django-compressor',
        'django-pyscss',
        'django_mobileesp',
        'django-templatetag-handlebars',
        'UW-RestClients-SWS',
        'UW-RestClients-PWS',
        'UW-Restclients-Django-Utils'
    ],
    license='Apache License, Version 2.0',  # example license
    description='A Django App for viewing course data',
    long_description=README,
    url='http://www.example.com/',
    author='UW IT AXDD',
    author_email='uw-it-aca@uw.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
