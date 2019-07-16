#! /usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='nete',
    version='0.1',
    author='Frank Ploss',
    author_email='nete@fqxp.de',
    license='GPL',
    url='https://github.com/fqxp/nete-gtk',
    install_requires=[
        'CommonMark',
        'pyrsistent',
        'termcolor',
    ],
    packages=find_packages(exclude=['*.tests']),
    package_data={
        'nete.gtkgui.resources': [
            '*',
        ],
    },
    entry_points={
        'gui_scripts': [
            'nete-gtk = nete.gtkgui.main:main',
        ],
    },
)
