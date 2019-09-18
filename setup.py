#!/usr/bin/env python
from setuptools import find_packages, setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='Flask-WX-OAuth',
    version='0.2.0',
    description='Flask Extension for wechat oauth2.0.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/Flask-WX-OAuth',
    license='MIT',
    install_requires=['requests'],
    packages=find_packages(),
)
