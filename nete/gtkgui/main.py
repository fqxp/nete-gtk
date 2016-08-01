import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .application import Application
import sys


def main():
    settings = Gtk.Settings.get_default()
    settings.set_property('gtk-theme-name', 'Adwaita')

    app = Application()
    exit_status = app.run(sys.argv)

    Gtk.main()

    sys.exit(exit_status)
