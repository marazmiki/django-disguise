#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


version = '0.2.1'


CLASSIFIERS = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Framework :: Django'
]


def long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
        return fp.read()

setup(
    name='django-disguise',
    author='Mikhail Porokhovnichenko',
    version=version,
    author_email='marazmiki@gmail.com',
    url='https://github.com/marazmiki/django-disguise',
    description=('This django application allows superuser to '
                 '"disguise" into any user'),
    long_description=long_description(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['test_project', 'test_project.*']),
    test_suite='tests.main',
    include_package_data=True,
    zip_safe=False
)
