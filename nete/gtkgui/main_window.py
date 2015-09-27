from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.note_list_view import NoteListView
from .note_text_view import NoteTextView
from .models.note_list import NoteList


class MainWindow(Gtk.Window, GObject.GObject):

    note_list = GObject.property(type=NoteList)

    __gsignals__ = {
        'next_note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev_note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, note_list):
        Gtk.Window.__init__(self, title='nete')

        self.note_list = note_list

        self.set_default_size(600, 350)

        self.build_ui()
        self.connect_signals()

        self.note_list.load()
        self.note_list_view.select_first()

    def build_ui(self):
        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.note_text_view = NoteTextView()
        self.grid.attach(self.note_text_view, 1, 0, 3, 1)

        self.note_list_view = NoteListView(self.note_list)
        self.grid.attach(self.note_list_view, 0, 0, 1, 1)

        self.add_accelerators()

    def connect_signals(self):
        self.note_list_view.connect('selection-changed', self.on_note_list_selection_changed)

    def add_accelerators(self):
        self.accel_group = Gtk.AccelGroup()
        self.add_accelerator('next_note',
                             self.accel_group,
                             Gdk.KEY_Page_Down,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('prev_note',
                             self.accel_group,
                             Gdk.KEY_Page_Up,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_next_note(self):
        self.note_list_view.select_next()

    def do_prev_note(self):
        self.note_list_view.select_previous()

    def on_note_list_selection_changed(self, source, note):
        self.note_text_view.text = note.text

