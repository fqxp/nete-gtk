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

    apt-get install python-markdown qml-module-qt-labs-settings \
        qml-module-qtquick2 qml-module-qtquick-window2 \
        qml-module-qtquick-controls qml-module-qtquick-layouts \
        fonts-font-awesome

The current version of PyQt5 shipped with Debian (5.3.2) is
[buggy](http://python.6.x6.nabble.com/Qml-Instantiate-a-model-derived-from-QAbstractListModel-from-qml-td5078937.html)
and nete-qt doesn‘t work with it. You need to download and [install
PyQt5 and SIP](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html).

An alternative is to use `schroot` to cleanly use stretch packags on a jessie
system.

### On Debian stretch (testing)

Install required Debian packages:

    apt-get install python-pyqt5 python-pyqt5.qtquick \
        python-markdown qml-module-qt-labs-settings \
        qml-module-qtquick2 qml-module-qtquick-window2 \
        qml-module-qtquick-controls qml-module-qtquick-layouts \
        qml-module-qtquick-dialogs fonts-font-awesome

## Install nete

After having fulfilled the dependencies, simply install by using setuptools:

    python setup.py install

You should now have the scripts `nete-qt` and `nete-cli` in your path.

# DBus interface

## Toggle main window
Use

    dbus-send --session --type=method_call --dest=de.fqxp.nete / de.fqxp.nete.MainController.toggle

to toggle the visibility of the main window.

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

    NETE_DIR=. nete-qt

# Make Debian package (for Debian 9/stretch only)

Install requirements

    apt-get install debhelper dh-python python-setuptools

This should do the trick:

    debian/rules binary

# Credits
* Notepad icon: http://pixabay.com/en/notepad-editor-pencil-document-97841/
