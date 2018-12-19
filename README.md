# What's nete?

nete (pronounce: neat) will be a nice, useful note-taking application suite.

It's currently in alpha state.

[![Build Status](https://travis-ci.org/fqxp/nete-gtk.svg?branch=master)](https://travis-ci.org/fqxp/nete-gtk)

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

## Install dependencies

### On Debian jessie
Install required Debian packages:

    apt-get install python3 gir1.2-webkit2-4.0

### On ArchLinux

Install packages from AUR:

* python
* webkit2gtk

## Install nete

After having fulfilled the dependencies, simply install by using setuptools:

    python setup.py install

You should now have the scripts `nete-gtk` and `nete-cli` in your path.

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

You can now run the tests like this:

    nosetests tests

Or you can run one of the clients using

    NETE_DIR=. nete-gtk

## Running tests

Run tests:

    (venv)$ nose2 -c nose2.cfg
