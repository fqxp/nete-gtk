from fluous.store import Store
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff
from .persistence.note_persistence import NotePersistence
from .persistence.ui_state_persistence import ConnectedUiStatePersistence
from .components.main_window import ConnectedMainWindow
from .state.action_types import *
from .state.actions import select_note, load_notes, load_ui_state
from .state import note_list


initial_state = {
    'storage_uri': 'nete:notes',
    'is_editing_title': False,
    'is_editing_text': False,
    'note_title': None,
    'note_text': None,
    'notes': [],
    'ui_state': {
        'current_note_id': None,
        'window_position': None,
        'window_size': [600, 400],
    },
}


# @log_traceback
@log_state_diff
@log_action
def reducer(state, action):
    action_type = action['type']

    if action_type == SELECT_NOTE:
        return state.update({
            'note_title': action['title'],
            'note_text': action['text'],
            'is_editing_title': False,
            'is_editing_text': False,
        }).set_by_path(
            ('ui_state', 'current_note_id'), action['note_id'])
    elif action_type == CREATE_NOTE:
        return state.update({
            'note_title': action['title'],
            'note_text': action['text'],
            'is_editing_title': True,
            'is_editing_text': False,
            'notes': note_list.add_new(
                state['notes'], action['note_id'], action['title'])
        }).set_by_path(
            ('ui_state', 'current_note_id'), action['note_id'])
    elif action_type == CHANGE_NOTE_TEXT:
        return state.set('note_text', action['text'])
    elif action_type == CHANGE_NOTE_TITLE:
        return state \
            .set('note_title', action['title']) \
            .set('notes',
                 note_list.ordered(
                    note_list.change_title(state['notes'], action['note_id'], action['title'])))
    elif action_type == TOGGLE_EDIT_NOTE_TEXT:
        return state \
            .set('is_editing_text', not state['is_editing_text']) \
            .set('is_editing_title', False)
    elif action_type == TOGGLE_EDIT_NOTE_TITLE:
        return state \
            .set('is_editing_title', not state['is_editing_title']) \
            .set('is_editing_text', False)
    elif action_type == FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)
    elif action_type == FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)
    elif action_type == LOADED_NOTES:
        return state.set('notes', note_list.ordered(action['notes']))
    elif action_type == MOVE_OR_RESIZE_WINDOW:
        return state \
            .set_by_path(('ui_state', 'window_position'), action['position']) \
            .set_by_path(('ui_state', 'window_size'), action['size'])
    elif action_type == LOADED_UI_STATE:
        new_ui_state = dict(state['ui_state'])
        new_ui_state.update(action['ui_state'])
        return state.set('ui_state', new_ui_state)
    else:
        return state


def relative_selection_middleware(state, action):
    action_type = action['type']

    if action_type == SELECT_FIRST:
        note_id = note_list.first_note_id(state['notes'])
        if note_id is not None:
            return select_note(note_id)
    elif action_type == SELECT_NEXT:
        note_id = note_list.next_note_id(
            state['notes'],
            state['ui_state']['current_note_id'])
        return select_note(note_id)
    elif action_type == SELECT_PREVIOUS:
        note_id = note_list.previous_note_id(
            state['notes'],
            state['ui_state']['current_note_id'])
        return select_note(note_id)
    else:
        return action


class Application:

    def __init__(self):
        store = Store(reducer, initial_state)
        store.add_middleware(relative_selection_middleware)

        store.dispatch(load_notes())
        store.dispatch(load_ui_state())

        self.persistence = NotePersistence(store)
        self.ui_persistence = ConnectedUiStatePersistence(store)

        self.main_window = ConnectedMainWindow(store)

    def show_window(self):
        self.main_window.show_all()
