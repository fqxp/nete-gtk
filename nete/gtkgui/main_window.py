from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.note_list_view import NoteListView
from .note_view import NoteView
from .models.note_list import NoteList


class MainWindow(Gtk.Window, GObject.GObject):

    note_list = GObject.property(type=NoteList)

    __gsignals__ = {
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-title-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, note_list):
        Gtk.Window.__init__(self, title='nete')

        self.note_list = note_list
        self._current_note = None
        self._note_attribute_changed_handler_id = None

        self.set_default_size(800, 450)

        self.build_ui()
        self.connect_signals()

        self.note_list.load()
        self.note_list_view.select_first()

    def build_ui(self):
        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.note_list_view = NoteListView(self.note_list)
        self.grid.attach(self.note_list_view, 0, 0, 1, 1)

        self.note_view = NoteView()
        self.grid.attach(self.note_view, 1, 0, 3, 1)

        self.add_accelerators()

    def connect_signals(self):
        self.note_list_view.connect('selection-changed',
                                    self.on_note_list_selection_changed)

    def add_accelerators(self):
        self.accel_group = Gtk.AccelGroup()
        self.add_accelerator('next-note',
                             self.accel_group,
                             Gdk.KEY_Page_Down,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('prev-note',
                             self.accel_group,
                             Gdk.KEY_Page_Up,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('toggle-edit-mode',
                             self.accel_group,
                             Gdk.KEY_Return,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('toggle-edit-title-mode',
                             self.accel_group,
                             ord('T'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('quit',
                             self.accel_group,
                             ord('Q'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_next_note(self):
        self.note_list_view.select_next()

    def do_prev_note(self):
        self.note_list_view.select_previous()

    def do_toggle_edit_mode(self):
        self.note_view.toggle_edit_mode()

    def do_toggle_edit_title_mode(self):
        self.note_view.toggle_title_mode()

    def do_quit(self):
        Gtk.main_quit()

    def on_note_list_selection_changed(self, source, note):
        self.grid.remove(self.note_view)
        self.note_view = NoteView(note)
        self.grid.attach(self.note_view, 1, 0, 3, 1)
        self.show_all()

        if self._note_attribute_changed_handler_id is not None:
            self._current_note.disconnect(self._note_attribute_changed_handler_id)
        self._note_attribute_changed_handler_id = note.connect('changed', self.on_note_attributes_changed)
        self._current_note = note

    def on_note_attributes_changed(self, obj, note):
        note.save()

