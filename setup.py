#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='Flask-WX-OAuth',
    version='0.1.1',
    description='Flask Extension for wechat oauth2.0.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/Flask-WX-OAuth',
    license='MIT',
    install_requires=['rauth'],
    packages=find_packages(),
)
