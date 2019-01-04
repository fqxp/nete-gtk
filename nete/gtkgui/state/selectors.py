from functools import lru_cache
from pyrsistent import freeze


@lru_cache()
def current_note(state):
    return freeze({
        'id': state['current_note']['id'],
        'title': state['current_note']['title'],
        'text': state['current_note']['text'],
        'cursor_position': state['current_note']['cursor_position'],
        'storage_uri': state['ui_state']['storage_uri'],
        'needs_save': state['current_note']['needs_save'],
    })


@lru_cache()
def ui_state(state):
    return state['ui_state']
