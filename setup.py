#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pip.req.req_file import parse_requirements
from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt', session=False)]
test_requirements = [str(ir.req) for ir in parse_requirements('requirements_dev.txt', session=False)]

setup(
    name='taxfix',
    version='0.9.0',
    description="Implement a batch job that transforms the given events predicting the following output and visualizing in any tool of our choice",
    long_description=readme,
    author="Robson Luis Monteiro Junior",
    author_email='bsao@icloud.com',
    url='https://github.com/bsao/taxfix',
    packages=[
        'taxfix',
        'taxfix.pipeline',
    ],
    package_dir={
        'taxfix': 'taxfix'
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='taxfix',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
