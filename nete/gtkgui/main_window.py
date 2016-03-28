from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.state.actions import (
    toggle_edit_note_text, toggle_edit_note_title, select_next,
    select_previous, create_note)
from .note_list_view import ConnectedNoteListView
from .note_view import NoteView
import pkg_resources


class MainWindow(Gtk.Window, GObject.GObject):

    __gsignals__ = {
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-title-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'create-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, store):
        Gtk.Window.__init__(self, title='nete')

        self.set_name('main-window')
        self.set_default_size(800, 450)

        self.build_ui(store)

        store.subscribe(self.set_state)
        self.connect_store(store)
        self.set_state(store.state)

    def set_state(self, state):
        if self.get_title() != self._make_title(state['note_title']):
            self.set_title(self._make_title(state['note_title']))

    def _make_title(self, note_title):
        return 'nete: %s' % note_title

    def connect_store(self, store):
        self.connect(
            'toggle-edit-mode',
            lambda source: store.dispatch(toggle_edit_note_text()))
        self.connect(
            'toggle-edit-title-mode',
            lambda source: store.dispatch(toggle_edit_note_title()))
        self.connect(
            'next-note',
            lambda source: store.dispatch(select_next()))
        self.connect(
            'prev-note',
            lambda source: store.dispatch(select_previous()))
        self.connect(
            'create-note',
            lambda source: store.dispatch(create_note()))

    def build_ui(self, store):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(pkg_resources.resource_filename(__name__, 'style/style.css'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.paned = Gtk.HPaned()
        self.add(self.paned)

        self.note_list_view = ConnectedNoteListView(store)
        self.note_list_view.set_size_request(180, -1)
        self.paned.add1(self.note_list_view)

        self.note_view = NoteView(store)
        self.paned.add2(self.note_view)

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
        self.add_accelerator('create-note',
                             self.accel_group,
                             ord('N'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('quit',
                             self.accel_group,
                             ord('Q'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_quit(self):
        Gtk.main_quit()
