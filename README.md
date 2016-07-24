# What's nete?

nete (pronounce: neat) will be a nice, useful note-taking application suite.

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

## Install dependencies

### On Debian jessie
Install required Debian packages:

    apt-get install python3 python3-markdown

## Install nete

After having fulfilled the dependencies, simply install by using setuptools:

    python setup.py install

You should now have the scripts `nete-qt` and `nete-cli` in your path.

# Development
First, set up a virtualenv to install required development packages into and
install development requirements:

    cd $PROJECT_DIR
    virtualenv --system-site-packages venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

Activate the virtual environment and run setup:

    ./venv/bin/activate:
    python setup.py develop

You can now run the tests like this:

    nosetests tests

Or you can run one of the clients using

    NETE_DIR=. nete-gtk

## Running tests

Run tests:

    (venv)$ nose2 -c nose2.cfg

# Make Debian package (for Debian 9/stretch only)

Install requirements

    apt-get install debhelper dh-python python-setuptools

This should do the trick:

    debian/rules binary

# Credits

* Notepad icon: http://pixabay.com/en/notepad-editor-pencil-document-97841/
