from gi.repository import Gtk
from nete.gtkgui.note_title_view import ConnectedNoteTitleView
from nete.gtkgui.note_text_view import ConnectedNoteTextView


class NoteView(Gtk.Grid):

    def __init__(self, store):
        super().__init__()

        self.build_ui(store)

    def build_ui(self, store):
        self.title_view = ConnectedNoteTitleView(store)
        self.attach(self.title_view, 0, 0, 1, 1)

        self.stack = ConnectedNoteTextView(store)
        self.attach(self.stack, 0, 1, 1, 1)

        self.show_all()
