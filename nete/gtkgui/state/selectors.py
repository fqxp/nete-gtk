from functools import lru_cache


@lru_cache()
def current_note(state):
    return {
        'id': state['current_note']['id'],
        'title': state['current_note']['note_title'],
        'text': state['current_note']['note_text'],
        'cursor_position': state['current_note']['cursor_position'],
        'storage_uri': state['ui_state']['storage_uri'],
        'needs_save': state['current_note']['needs_save'],
    }


@lru_cache()
def ui_state(state):
    return state['ui_state']
