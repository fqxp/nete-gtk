from gi.repository import Gtk
from nete.gtkgui.application import Application


def main():
    settings = Gtk.Settings.get_default()
    settings.set_property('gtk-theme-name', 'Adwaita')

    app = Application()
    app.show_window()

    Gtk.main()

