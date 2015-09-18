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

setup(
    name='gmailbackup',
    version='1.0.2',

    author='Chris Lyon',
    author_email='flushot@gmail.com',
    url='https://github.com/Flushot/gmailbackup',

    description='Gmail Backup',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators'
    ],
    
    entry_points={
        'console_scripts': [
            'gmailbackup=gmailbackup:main'
        ]
    },

    install_requires=[
        'argparse'
    ],

    test_suite='test'
)
