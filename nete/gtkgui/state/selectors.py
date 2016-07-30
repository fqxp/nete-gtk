from functools import lru_cache


@lru_cache()
def current_note(state):
    return {
        'id': state['current_note']['id'],
        'title': state['current_note']['note_title'],
        'text': state['current_note']['note_text'],
        'storage_uri': state['ui_state']['storage_uri'],
        'needs_save': state['current_note']['needs_save'],
    }
