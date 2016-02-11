from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.note_list_view import NoteListView
from nete.gtkgui.state.actions import (
    select_note, toggle_edit_note_text, toggle_edit_note_title)
from .note_view import NoteView
from .models.note_list import NoteList
import pkg_resources


class MainWindow(Gtk.Window, GObject.GObject):

    note_list = GObject.property(type=NoteList)

    __gsignals__ = {
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-title-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, store, note_list):
        Gtk.Window.__init__(self, title='nete')

        self.set_name('main-window')

        self.note_list = note_list
        self._current_note = None
        self._note_attribute_changed_handler_id = None

        self.set_default_size(800, 450)

        self.build_ui(store)

        self.note_list.load()
        self.note_list_view.select_first()

        store.subscribe(self.on_state_changed)
        self.connect_store(store)

    def on_state_changed(self, state):
        print('NEW STATE: % s', state)

    def connect_store(self, store):
        self.note_list_view.connect(
            'selection-changed',
            lambda source, note: store.dispatch(select_note(note.id)))
        self.connect(
            'toggle-edit-mode',
            lambda source: store.dispatch(toggle_edit_note_text()))
        self.connect(
            'toggle-edit-title-mode',
            lambda source: store.dispatch(toggle_edit_note_title()))

    def build_ui(self, store):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(pkg_resources.resource_filename(__name__, 'style/style.css'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.paned = Gtk.HPaned()
        self.add(self.paned)

        self.note_list_view = NoteListView(self.note_list)
        self.note_list_view.set_size_request(180, -1)
        self.paned.add1(self.note_list_view)

        self.note_view = NoteView(store)
        self.paned.add2(self.note_view)

        # self.show_all()

        self.add_accelerators()

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

    def do_quit(self):
        Gtk.main_quit()

    def on_note_list_selection_changed(self, source, note):
        if self.note_view is None:
            self.note_view = NoteView(note)
            self.paned.add2(self.note_view)
            self.show_all()
        else:
            self.note_view.set_note(note)

        if self._note_attribute_changed_handler_id is not None:
            self._current_note.disconnect(self._note_attribute_changed_handler_id)
        self._note_attribute_changed_handler_id = note.connect('changed', self.on_note_attributes_changed)
        self._current_note = note

    def on_note_attributes_changed(self, note):
        note.save()

