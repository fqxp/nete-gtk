from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.state.actions import (
    toggle_edit_note_text, toggle_edit_note_title, select_next,
    select_previous, create_note)
from fluous.gobject import connect
from .note_list_view import ConnectedNoteListView
from .note_view import NoteView
import pkg_resources


def map_state_to_props(state):
    return (
        ('title', 'nete: %s' % state['note_title']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'toggle-edit-mode': lambda source: dispatch(toggle_edit_note_text()),
        'toggle-edit-title-mode': lambda source: dispatch(toggle_edit_note_title()),
        'next-note': lambda source: dispatch(select_next()),
        'prev-note': lambda source: dispatch(select_previous()),
        'create-note': lambda source: dispatch(create_note()),
    }


class MainWindow(Gtk.Window):
    __gsignals__ = {
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-title-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'create-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, build_component):
        Gtk.Window.__init__(self, title='nete')

        self.set_name('main-window')
        self.set_default_size(800, 450)

        self.set_property('title', 'AARRGGHH')

        self._build_ui(build_component)

    def _build_ui(self, build_component):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(pkg_resources.resource_filename(__name__, 'style/style.css'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.paned = Gtk.HPaned()
        self.add(self.paned)

        self.note_list_view = build_component(ConnectedNoteListView)
        self.note_list_view.set_size_request(180, -1)
        self.paned.add1(self.note_list_view)

        self.note_view = build_component(NoteView)
        self.paned.add2(self.note_view)

        self._add_accelerators()

    def _add_accelerators(self):
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


ConnectedMainWindow = connect(MainWindow, map_state_to_props, map_dispatch_to_props)
