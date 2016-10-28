from gi.repository import Gdk, Gtk, GObject
from nete.gtkgui.actions import (
    move_paned, quit, create_note,
    toggle_edit_mode_text, toggle_edit_mode_title,
    next_note, prev_note,
    set_filter_term_entry_focus)
from .note_list_view import create_note_list_view
from .note_view import create_note_view
from .note_title_view import create_note_title_view
from flurx import create_component


def create_note_window(store):
    note_list_view = create_note_list_view(store)
    note_view = create_note_view(store)
    note_title_view = create_note_title_view(store)

    return create_component(
        NoteWindow, store, map_state_to_props,
        note_list_view=note_list_view,
        note_view=note_view,
        note_title_view=note_title_view
    )


def map_state_to_props(state):
    return (
        ('paned-position', state['ui_state']['paned_position']),
    )


class NoteWindow(Gtk.Window):

    paned_position = GObject.property(type=int)

    __gsignals__ = {
        'create-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-text-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'toggle-title-edit-mode': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'next-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'prev-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'focus-filter-term-entry': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'print-marker': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
        'quit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, note_list_view, note_view, note_title_view):
        super().__init__()
        self.note_list_view = note_list_view
        self.note_view = note_view
        self.note_title_view = note_title_view
        self._build_ui()
        self._connect_events()
        self._add_accelerators()

    def _connect_events(self):
        self.connect('delete-event', lambda source, param: quit())

        self.connect('create-note', lambda *args: create_note())
        self.connect('toggle-text-edit-mode', lambda *args: toggle_edit_mode_text())
        self.connect('toggle-title-edit-mode', lambda *args: toggle_edit_mode_title())
        self.connect('next-note', lambda *args: next_note())
        self.connect('prev-note', lambda *args: prev_note())
        self.connect('focus-filter-term-entry', lambda *args: set_filter_term_entry_focus(True))
        self.connect('print-marker', lambda source: print('*' * 60))
        self.connect('quit', lambda source: quit())
        self.paned.connect('notify::position', self._on_paned_moved)
        self.bind_property('paned-position', self.paned, 'position', GObject.BindingFlags.BIDIRECTIONAL)

    def _on_paned_moved(self, *args):
        move_paned(self.paned.get_property('position'))

    def _build_ui(self):
        self.paned = Gtk.HPaned()
        self.add(self.paned)

        right_side = Gtk.Grid()
        right_side.attach(self.note_title_view, 0, 0, 1, 1)
        right_side.attach(self.note_view, 0, 1, 1, 1)

        self.paned.add1(self.note_list_view)
        self.paned.add2(right_side)

    def _add_accelerators(self):
        accel_group = Gtk.AccelGroup()

        self.add_accelerator('create-note',
                             accel_group,
                             ord('N'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('toggle-text-edit-mode',
                             accel_group,
                             Gdk.KEY_Return,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('toggle-title-edit-mode',
                             accel_group,
                             ord('T'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('next-note',
                             accel_group,
                             Gdk.KEY_Page_Down,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('prev-note',
                             accel_group,
                             Gdk.KEY_Page_Up,
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('focus-filter-term-entry',
                             accel_group,
                             ord('F'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('quit',
                             accel_group,
                             ord('Q'),
                             Gdk.ModifierType.CONTROL_MASK,
                             Gtk.AccelFlags.VISIBLE)
        self.add_accelerator('print-marker',
                             accel_group,
                             ord('P'),
                             Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.SHIFT_MASK,
                             Gtk.AccelFlags.VISIBLE)

        self.add_accel_group(accel_group)
