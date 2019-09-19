#!/usr/bin/env python
import re
from setuptools import find_packages, setup

with open('flask_wx_oauth/__init__.py', encoding='utf-8') as f:
    version = re.search(r"__version__\s*=\s*'([\w\-.]+)'", f.read()).group(1)
    assert version

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='Flask-WX-OAuth',
    version=version,
    url='https://github.com/codeif/Flask-WX-OAuth',
    project_urls={
        "Documentation": "https://flask-wx-oauth.readthedocs.io",
    },
    description='Flask Extension for wechat oauth2.0.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    license='MIT',
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
)
