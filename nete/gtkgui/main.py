import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk
import sys

from .application import Application


def main():
    settings = Gtk.Settings.get_default()
    settings.set_property('gtk-theme-name', 'Adwaita')

    app = Application()
    exit_status = app.run(sys.argv)

    Gtk.main()

    sys.exit(exit_status)
