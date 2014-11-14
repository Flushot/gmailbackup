#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Allow trove classifiers in previous python versions
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

from gmailbackup import __version__ as version

setup(
    name='gmailbackup',
    version=version,

    author='Chris Lyon',
    author_email='flushot@gmail.com',

    description='Gmail Backup',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators'
    ],
    
    scripts=[
        'gmailbackup'
    ],

    install_requires=[
        'argparse'
    ],

    test_suite='test'
)
