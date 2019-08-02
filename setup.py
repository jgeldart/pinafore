#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
from setuptools import setup, find_namespace_packages

VERSIONFILE = "src/pinafore/__init__.py"
VERSION = None
for line in open(VERSIONFILE, "r").readlines():
    if line.startswith('__version__'):
        VERSION = line.split('"')[1]

if not VERSION:
    raise RuntimeError('No version defined in pinafore.__init__.py')

README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'),
                     'r', encoding='utf-8').read()

setup(
    name='pinafore',
    version=VERSION,
    description='A parser library for Notation4',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Joe Geldart',
    author_email='joe@joegeldart.com',
    license='MIT',
    url='https://github.com/jgeldart/pinafore',
    download_url='https://github.com/jgeldart/pinafore/archive/v%s.tar.gz'
        % VERSION,
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=["textX>=2.0.0"],
    tests_require=[
        'pytest',
    ],
    keywords="parser notation4 rdf semantic-web",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]

)