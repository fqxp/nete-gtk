#! /usr/bin/env python3
from setuptools import setup, find_packages


setup(
    name='nete',
    version='0.1',
    author='Frank Ploss',
    author_email='nete@fqxp.de',
    license='GPL',
    url='https://github.com/fqxp/nete-gtk',
    packages=find_packages(),
    package_data={
        '': ['*.png'],
        'nete.gtkgui': [
        ],
    },
    entry_points={
        'gui_scripts': [
            'nete-gtk = nete.gtkgui.main:main',
        ],
        'console_scripts': [
            'nete-cli = nete.cli.main:main',
        ],
    },
)
