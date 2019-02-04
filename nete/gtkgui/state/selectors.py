from functools import lru_cache


@lru_cache()
def current_note(state):
    return state.get('current_note')


@lru_cache()
def ui_state(state):
    return state['ui']
