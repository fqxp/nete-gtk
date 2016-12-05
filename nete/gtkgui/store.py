from pyrsistent import freeze
from rx.subjects import BehaviorSubject


initial_state = {
    'cache': {
        'notes': [],
    },
    'current_note': {
        'id': None,
        'note_title': '',
        'note_text': '',
        'cursor_position': 0,
        'needs_save': False,
    },
    'ui_state': {
        'storage_uri': 'nete:notes',
        'is_editing_title': False,
        'is_editing_text': False,
        'current_note_id': None,
        'paned_position': 250,
        'filter_term_entry_focus': False,
        'filter_term': '',
   },
}


store = BehaviorSubject(freeze(initial_state))
