from fluous.gobject import connect
from gi.repository import Gtk, GObject
from .filter_view import FilterView
from .note_list_view import NoteListView
from ..actions import (
    change_filter_term,
    choose_preselected_note,
    create_note,
    focus_filter_term_entry,
    preselect_note,
    preselect_next,
    preselect_previous,
    load_note
)


class NoteChooser(Gtk.Grid):

    notes = GObject.Property(type=GObject.TYPE_PYOBJECT)
    current_note_title = GObject.Property(type=str, default='')
    filter_term = GObject.Property(type=str, default='')
    has_focus = GObject.Property(type=bool, default=False)
    preselected_note_title = GObject.Property(type=str, default='')

    __gsignals__ = {
        'select-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str,)),
        'create-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, ()),
        'filter-term-changed':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str,)),
        'filter-term-entry-focused':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'preselect-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str,)),
        'preselect-next-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'preselect-previous-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'select-preselected-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
    }

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.set_name('note-list-view')

        self._build_ui(build_component)
        self._connect_events()

    def _build_ui(self, build_component):
        self.filter_view = FilterView()
        self.attach(self.filter_view, 0, 0, 1, 1)

        self.scrollable_treelist = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True,
            can_focus=False)
        self.attach(self.scrollable_treelist, 0, 1, 1, 1)

        self.note_list_view = NoteListView(
            notes=self.get_property('notes'),
            current_note_title=self.get_property('current_note_title'),
            preselected_note_title=self.get_property('preselected_note_title')
        )
        self.scrollable_treelist.add(self.note_list_view)

        self.create_button = Gtk.Button('New Note')
        self.attach(self.create_button, 0, 2, 1, 1)

        self.set_focus_chain([])

    def _connect_events(self):
        self.create_button.connect(
            'clicked',
            lambda source: self.emit('create-note'))

        self.note_list_view.connect(
            'preselect-note',
            lambda source, note_title: self.emit('preselect-note', note_title))
        self.note_list_view.connect(
            'select-note',
            lambda source, note_title: self.emit('select-note', note_title))

        self.bind_property('notes',
                           self.note_list_view,
                           'notes',
                           GObject.BindingFlags.DEFAULT)
        self.bind_property('current-note-title',
                           self.note_list_view,
                           'current-note-title',
                           GObject.BindingFlags.DEFAULT)
        self.bind_property('preselected-note-title',
                           self.note_list_view,
                           'preselected-note-title',
                           GObject.BindingFlags.DEFAULT)
        self.bind_property('filter-term',
                           self.filter_view,
                           'filter-term',
                           GObject.BindingFlags.DEFAULT)
        self.bind_property('has-focus',
                           self.filter_view,
                           'has-focus',
                           GObject.BindingFlags.DEFAULT)

        self.filter_view.connect(
            'filter-term-changed',
            lambda source, filter_term: (
                self.emit('filter-term-changed', filter_term)))
        self.filter_view.connect(
            'focused', lambda source: (
                self.emit('filter-term-entry-focused')))
        self.filter_view.connect(
            'keyboard-down', lambda source: (
                self.emit('preselect-next-note')))
        self.filter_view.connect(
            'keyboard-up', lambda source: (
                self.emit('preselect-previous-note')))
        self.filter_view.connect(
            'select-preselected-note', lambda source: (
                self.emit('select-preselected-note')))


def map_state_to_props(state):
    return (
        ('notes', state['note_list']['notes']),
        ('current-note-title', (
            state['current_note']['title']
            if state['current_note']
            else None)),
        ('filter-term', state['note_list']['filter_term']),
        ('has-focus', state['ui']['focus'] == 'filter_term'),
        ('preselected-note-title', (
            state['note_list']['preselected_note_title'])),
    )


def map_dispatch_to_props(dispatch):
    return {
        'select-note': lambda source, note_title: (
            dispatch(load_note(note_title))),
        'create-note': lambda source: (
            dispatch(create_note())),
        'filter-term-changed': lambda source, filter_term: (
            dispatch(change_filter_term(filter_term))),
        'filter-term-entry-focused': lambda source: (
            dispatch(focus_filter_term_entry())),
        'preselect-note': lambda source, note_title: (
            dispatch(preselect_note(note_title))),
        'preselect-next-note': lambda source: (
            dispatch(preselect_next())),
        'preselect-previous-note': lambda source: (
            dispatch(preselect_previous())),
        'select-preselected-note': lambda source: (
            dispatch(choose_preselected_note())),
    }


ConnectedNoteChooser = connect(
    NoteChooser,
    map_state_to_props,
    map_dispatch_to_props)
