#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='chomskyday',
    version='0.1.dev',
    description='Create and personalise a Google Calendar',
    author='Eyal Kazin',
    author_email='eyalkazin@gmail.com',
    install_requires=['requests >= 2.14', 'httplib2 >= 0.10','google-api-python-client >= 1.6.2', 
                        'oauth2client >= 4.1',  'argparse >= 1.1'],
    packages=find_packages(),
    #include_package_data=True
)