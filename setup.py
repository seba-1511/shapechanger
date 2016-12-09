#!/usr/bin/env python

import os
from distutils.core import setup
from setuptools import (
    setup as install,
    find_packages,
)

VERSION = '0.1.0'

setup(
      name='mj_transfer',
)
install(
    name='mj_transfer',
    version=VERSION,
    description="Easy Transfer Learning environments for OpenAI Gym built on top of MuJoCo",
    long_description=open('README.md').read(),
    author='Elizabeth Chu, Seb Arnold',
    author_email='smr.arnold@gmail.com',
    license='License :: OSI Approved :: Apache Software License',
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        'Tools',
        ]
)
