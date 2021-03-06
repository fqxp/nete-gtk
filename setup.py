#! /usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='nete',
    version='0.1',
    author='Frank Ploss',
    author_email='frank@fqxp.de',
    license='GPL',
    url='https://github.com/fqxp/nete-gtk',
    install_requires=[
        'mistune>=0.8,<2.0',
        'pyrsistent>=0.14',
        'cairocffi>=1.0',
        'PyGObject>=3.30',
        'pycairo>=1.16',
    ],
    packages=find_packages(
        exclude=[
            'tests',
            'fluous.tests',
        ],
    ),
    package_data={
        'nete.resources': [
            '*/*.css',
            '*/*.html',
            '*/*.lang',
            '*/*.xml',
        ],
    },
    extras_require={
        'dev': [
            'deepdiff>=1.1',
            'mock>=1.0',
            'pycodestyle>=2.5',
            'termcolor>=1.1',
            'pytest>=5.0.1',
        ],
    },
    entry_points={
        'gui_scripts': [
            'nete-gtk = nete.main:main',
        ],
    },
)
