from gi.repository import Gtk
from nete.gtkgui.models.note_list import NoteList
from nete.gtkgui.main_window import MainWindow


class Application:

    def __init__(self):
        note_list = NoteList('nete:notes')
        note_list.load()
        self.main_window = MainWindow(note_list)
        self.main_window.connect("delete-event", Gtk.main_quit)

    def show_window(self):
        self.main_window.show_all()
