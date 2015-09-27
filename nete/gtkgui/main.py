from gi.repository import Gtk
from nete.gtkgui.application import Application


def main():
    app = Application()
    app.show_window()

    Gtk.main()

