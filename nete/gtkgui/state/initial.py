from pyrsistent import PRecord, field, pvector_field


class Note(PRecord):
    id = field(type=(str, type(None)))
    title = field(type=(str, type(None)))
    text = field(type=(str, type(None)))
    cursor_position = field(type=int)
    needs_save = field(type=bool)


class Cache(PRecord):
    notes = pvector_field(Note)


class UiState(PRecord):
    storage_uri = field(type=(str, type(None)))
    is_editing_title = field(type=bool)
    is_editing_text = field(type=bool)
    current_note_id = field(type=(str, type(None)))
    paned_position = field(type=int)
    filter_term_entry_focus = field(type=bool)
    filter_term = field(type=str)


class State(PRecord):
    cache = field(type=Cache)
    current_note = field(type=(Note, type(None)))
    ui_state = field(type=UiState)


initial_state = State.create({
    'cache': Cache.create({
        'notes': [],
    }),
    'current_note': Note.create({
        'id': None,
        'title': None,
        'text': None,
        'cursor_position': 0,
        'needs_save': False,
    }),
    'ui_state': UiState.create({
        'storage_uri': 'nete:notes',
        'is_editing_title': False,
        'is_editing_text': False,
        'current_note_id': None,
        'paned_position': 250,
        'filter_term_entry_focus': False,
        'filter_term': '',
    }),
})
