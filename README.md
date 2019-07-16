[![Build Status](https://travis-ci.org/fqxp/nete-gtk.svg?branch=master)](https://travis-ci.org/fqxp/nete-gtk)

# What is nete?

nete (pronounce: neat) will be a nice, useful note-taking application.

It's currently in alpha state.

## Plans

nete will:
* be easy to use
* have a clean interface
* never forget anything you typed
* have multiple interfaces, like graphical, command line, or HTTP/AJAX
* encrypt notes using GnuPG if wanted
* synchronize notes using a central server or client-to-client
* ...

# Installation

## Package dependencies

### Debian jessie

Install Debian packages:

* python3
* gir1.2-webkit2-4.0
* gir1.2-gtksource-4

### ArchLinux

Install packages from AUR:

* python
* webkit2gtk
* gtksourceview4

## Install

Install using setuptools:

    ./setup.py install

You should now have the script `nete-gtk` in your path.

## Running the application

Run `nete-gtk` to start the application.

# Development
First, set up a virtualenv to install required development packages into and
install development requirements:

    cd $PROJECT_DIR
    virtualenv --system-site-packages venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

Activate the virtual environment and run setup:

    ./venv/bin/activate
    python setup.py egg_info -b dev develop

The `-b dev` adds the string `"dev"` to the version, which is important if you
want to run an installed version of nete and a version you’re developing on at
the same time.

Run the application:

    (venv)$ NETE_DIR=. nete-gtk

## Running tests

Run tests:

    (venv)$ pytest
