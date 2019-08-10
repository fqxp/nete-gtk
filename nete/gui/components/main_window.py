import logging

from fluous.gobject import connect
from gi.repository import Gdk, Gtk, GObject

from nete.gui.actions import (
    close_note,
    create_note,
    focus,
    move_note_to_trash,
    move_paned_position,
    reset,
    select_next,
    select_previous,
    toggle_edit_note_text,
    toggle_edit_note_title,
    zoom_in,
    zoom_out,
    zoom_reset,
)
from nete.gui.resources import stylesheet_filename
from nete.gui.components.focus_manager import FocusManager
from nete.gui.components.header_bar import ConnectedHeaderBar
from nete.gui.components.note_chooser import ConnectedNoteChooser
from nete.gui.components.note_view import ConnectedNoteView


logger = logging.getLogger(__name__)


class MainWindow(Gtk.ApplicationWindow):

    focus = GObject.Property(type=str)
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
        'move-note-to-trash':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'close-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'focus-filter-term-entry':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'focus-note-collection-chooser':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'quit':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'move-paned':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (int,)),
        'reset':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'zoom-in':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'zoom-out':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'zoom-reset':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
    }

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.set_name('main-window')

        self.focus_manager = FocusManager(self)
        self._build_ui(build_component)
        self._connect_events()

    def _connect_events(self):
        self.connect('delete-event', lambda source, param: self.do_quit())
        self.paned.connect('notify::position', self._on_paned_moved)
        self._notify_paned_position_handler = self.connect(
            'notify::paned-position',
            self._on_notify_paned_position
        )
        self.bind_property(
            'focus',
            self.focus_manager,
            'focus',
            GObject.BindingFlags.DEFAULT)

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
            'move-note-to-trash',
            self.accel_group,
            ord('D'),
            Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'close-note',
            self.accel_group,
            ord('W'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'focus-filter-term-entry',
            self.accel_group,
            ord('F'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'focus-note-collection-chooser',
            self.accel_group,
            ord('K'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'reset',
            self.accel_group,
            Gdk.KEY_Escape,
            0,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'quit',
            self.accel_group,
            ord('Q'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'zoom-in',
            self.accel_group,
            ord('+'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'zoom-out',
            self.accel_group,
            ord('-'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accelerator(
            'zoom-reset',
            self.accel_group,
            ord('0'),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE)
        self.add_accel_group(self.accel_group)

    def do_quit(self):
        self.props.application.quit()


def map_state_to_props(state):
    return (
        ('paned_position', state['ui']['paned_position']),
        ('focus', state['ui']['focus']),
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
        'move-note-to-trash':
            lambda source: dispatch(move_note_to_trash()),
        'close-note':
            lambda source: dispatch(close_note()),
        'focus-filter-term-entry':
            lambda source, s1: dispatch(focus('filter_term_entry')),
        'focus-note-collection-chooser':
            lambda source, _: dispatch(focus('note_collection_selector')),
        'move-paned':
            lambda source, position: dispatch(move_paned_position(position)),
        'reset':
            lambda source: dispatch(reset()),
        'zoom-in':
            lambda source: dispatch(zoom_in()),
        'zoom-out':
            lambda source: dispatch(zoom_out()),
        'zoom-reset':
            lambda source: dispatch(zoom_reset()),
    }


ConnectedMainWindow = connect(
    MainWindow,
    map_state_to_props,
    map_dispatch_to_props)
