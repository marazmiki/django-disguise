#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os


version = '0.0.3'


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django'
]


setup(
    name='django-disguise',
    author='marazmiki',
    version=version,
    author_email='marazmiki@gmail.com',
    url='http://pypi.python.org/pypi/django-disguise',
    download_url='http://bitbucket.org/marazmiki/django-disguise/get/tip.zip',
    description='This django application allows superuser to "disguise" into any user',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['test_project', 'test_project.*']),
    test_suite='tests.main',
    include_package_data=True,
    zip_safe=False
)
