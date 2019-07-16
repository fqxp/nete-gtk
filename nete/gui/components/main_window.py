import logging

from fluous.gobject import connect
from gi.repository import Gdk, Gtk, GObject

from nete.gui.actions import (
    create_note,
    delete_note,
    move_paned_position,
    select_next,
    select_previous,
    focus_filter_term_entry,
    toggle_edit_note_text,
    toggle_edit_note_title)
from nete.gui.resources import stylesheet_filename
from .header_bar import ConnectedHeaderBar
from .note_chooser import ConnectedNoteChooser
from .note_view import ConnectedNoteView


logger = logging.getLogger(__name__)


class MainWindow(Gtk.Window):
    paned_position = GObject.Property(type=int)

    __gsignals__ = {
        'next-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'prev-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'toggle-edit-mode':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'toggle-edit-title-mode':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'create-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'delete-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'focus-filter-term-entry':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'quit':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'move-paned':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (int,)),
        'print-marker':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'reset':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
    }

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.set_name('main-window')

        self._build_ui(build_component)
        self._connect_events()

    def _connect_events(self):
        self.connect('delete-event', lambda source, param: self.do_quit())
        self.connect('print-marker', lambda source: print('*' * 80))
        self.connect('reset', lambda source: logger.debug('RESET' * 80))
        self.paned.connect('notify::position', self._on_paned_moved)
        self._notify_paned_position_handler = self.connect(
            'notify::paned-position',
            self._on_notify_paned_position
        )

    def _on_paned_moved(self, source, param):
        with self.handler_block(self._notify_paned_position_handler):
            self.emit('move-paned', self.paned.get_property('position'))

    def _on_notify_paned_position(self, source, param):
        self.paned.set_property(
            'position',
            self.get_property('paned_position'))

    def _build_ui(self, build_component):
        self.set_default_size(800, 600)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(stylesheet_filename('application'))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.header_bar = build_component(ConnectedHeaderBar)
        self.set_titlebar(self.header_bar)

        self.paned = Gtk.HPaned(position=self.paned_position)
        self.add(self.paned)

        self.note_chooser = build_component(ConnectedNoteChooser)
        self.paned.add1(self.note_chooser)
        self.paned.child_set_property(self.note_chooser, 'shrink', False)

        self.note_view = build_component(ConnectedNoteView)
        self.paned.add2(self.note_view)

        self._add_accelerators()

    def _add_accelerators(self):
        self.accel_group = Gtk.AccelGroup()
        self.add_accelerator(
            'next-note',
            self.accel_group,
            Gdk.KEY_Page_Down,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'prev-note',
            self.accel_group,
            Gdk.KEY_Page_Up,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'toggle-edit-mode',
            self.accel_group,
            Gdk.KEY_Return,
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'toggle-edit-title-mode',
            self.accel_group,
            ord('T'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'create-note',
            self.accel_group,
            ord('N'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'delete-note',
            self.accel_group,
            ord('D'),
            Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'focus-filter-term-entry',
            self.accel_group,
            ord('F'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'quit',
            self.accel_group,
            ord('Q'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'print-marker',
            self.accel_group,
            ord('P'),
            Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_quit(self):
        Gtk.main_quit()


def map_state_to_props(state):
    return (
        ('paned_position', state['ui']['paned_position']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'toggle-edit-mode':
            lambda source: dispatch(toggle_edit_note_text()),
        'toggle-edit-title-mode':
            lambda source: dispatch(toggle_edit_note_title()),
        'next-note':
            lambda source: dispatch(select_next()),
        'prev-note':
            lambda source: dispatch(select_previous()),
        'create-note':
            lambda source: dispatch(create_note()),
        'delete-note':
            lambda source: dispatch(delete_note()),
        'focus-filter-term-entry':
            lambda source, s1: dispatch(focus_filter_term_entry()),
        'move-paned':
            lambda source, position: dispatch(move_paned_position(position)),
    }


ConnectedMainWindow = connect(
    MainWindow,
    map_state_to_props,
    map_dispatch_to_props)