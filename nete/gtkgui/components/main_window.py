from gi.repository import Gtk, Gdk, GObject
from nete.gtkgui.actions import (
    toggle_edit_note_text, toggle_edit_note_title, select_next,
    select_previous, create_note, delete_note, move_paned_position,
    set_filter_term_entry_focus)
from fluous.gobject import connect
from .header_bar import ConnectedHeaderBar
from .note_list_view import ConnectedNoteListView
from .note_view import NoteView
import logging
import pkg_resources


logger = logging.getLogger(__name__)


class MainWindow(Gtk.Window):
    paned_position = GObject.property(type=int)

    __gsignals__ = {
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-edit-title-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'create-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'delete-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'focus-filter-term-entry': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'move-paned': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (int,)),
        'print-marker': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'reset': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, build_component):
        Gtk.Window.__init__(self)

        self.set_name('main-window')

        self._build_ui(build_component)
        self._connect_events()

    def _connect_events(self):
        self.connect('delete-event', lambda source, param: self.do_quit())
        self.connect('print-marker', lambda source: print('*' * 80))
        self.connect('reset', lambda source: logger.debug('RESET' * 80))
        self.paned.connect('notify::position', self._on_paned_moved)
        self._notify_paned_position_handler = self.connect('notify::paned-position', self._on_notify_paned_position)

    def _on_paned_moved(self, source, param):
        with self.handler_block(self._notify_paned_position_handler):
            self.emit('move-paned', self.paned.get_property('position'))

    def _on_notify_paned_position(self, source, param):
        self.paned.set_property('position', self.get_property('paned_position'))

    def _build_ui(self, build_component):
        self.set_default_size(800, 600)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(pkg_resources.resource_filename('nete.gtkgui', 'style/style.css'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.header_bar = build_component(ConnectedHeaderBar)
        self.set_titlebar(self.header_bar)

        self.paned = Gtk.HPaned()
        self.add(self.paned)

        self.note_list_view = build_component(ConnectedNoteListView)
        self.paned.add1(self.note_list_view)
        self.paned.child_set_property(self.note_list_view, 'shrink', False)

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
        self.add_accelerator('delete-note',
                             self.accel_group,
                             ord('D'),
                             Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('focus-filter-term-entry',
                             self.accel_group,
                             ord('F'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('reset',
                             self.accel_group,
                             Gdk.KEY_Escape,
                             0,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('quit',
                             self.accel_group,
                             ord('Q'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('print-marker',
                             self.accel_group,
                             ord('P'),
                             Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_quit(self):
        Gtk.main_quit()


def map_state_to_props(state):
    return (
        ('paned-position', state['ui_state']['paned_position']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'toggle-edit-mode': lambda source: dispatch(toggle_edit_note_text()),
        'toggle-edit-title-mode': lambda source: dispatch(toggle_edit_note_title()),
        'next-note': lambda source: dispatch(select_next()),
        'prev-note': lambda source: dispatch(select_previous()),
        'create-note': lambda source: dispatch(create_note()),
        'delete-note': lambda source: dispatch(delete_note()),
        'focus-filter-term-entry': lambda source, s1: dispatch(set_filter_term_entry_focus(True)),
        'move-paned': lambda source, position: dispatch(move_paned_position(position)),
    }


ConnectedMainWindow = connect(MainWindow, map_state_to_props, map_dispatch_to_props)
