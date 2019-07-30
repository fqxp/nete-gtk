[![Build Status](https://travis-ci.org/fqxp/nete-gtk.svg?branch=master)](https://travis-ci.org/fqxp/nete-gtk)

# NOTE: THIS IS NOT FOR PUBLIC USE YET

# What is nete?

nete (pronounce: neat) will be a easy-to-use, useful note-taking
application.

It's currently in pre-alpha state.

## Plans

nete possibly will:
* be easy to use
* have a clean interface
* never forget anything you typed
* have multiple interfaces, like graphical, command line, or HTTP/AJAX
* encrypt notes using GnuPG if desired
* synchronize notes using an external tool like SyncThing, OwnCloud/Nextcloud or
  the like
* and a few more

# Installation

Assume `$PROJECT_DIR` is the directory you cloned this repository into.

## Package dependencies

### Debian jessie

Install Debian packages:

    $ sudo apt-get install python3 gir1.2-webkit2-4.0 \
      gir1.2-gtksource-4

### ArchLinux

Install packages:

    $ sudo pacman -S python webkit2gtk gtksourceview4

## Install

Change into project directory and install using setuptools:

    $ cd $PROJECT_DIR
    $ ./setup.py install --user

You should now have the script `nete-gtk` in your path. Run it!

# Development

## Development Setup

First, set up a virtualenv to install required development packages
into and install development requirements:

    $ cd $PROJECT_DIR
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt -r requirements-dev.txt

You should now have the `nete-gtk` script installed in the virtual
environment.

Run the application:

    (venv)$ nete-gtk

For the interesting debug info (including actions and state changes),
run:

    (venv)$ nete-gtk --debug

To additionally output tracebacks at action dispatch time, run:

    (venv)$ nete-gtk --debug --traceback

## Running tests

Run tests:

    (venv)$ pytest

## Create a binary distribution

Run:

    $ ./setup.py bdist_egg
