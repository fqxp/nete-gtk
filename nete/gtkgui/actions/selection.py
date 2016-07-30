from .action_types import ActionType
from nete.services.storage_factory import create_storage
from nete.gtkgui.state import note_list


def select_note(note_id):
    def load_note(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        note = storage.load(note_id)

        dispatch({
            'type': ActionType.SELECT_NOTE,
            'id': note['id'],
            'title': note['title'],
            'text': note['text'],
        })

    return load_note


def select_first():
    def select_first(dispatch, state):
        note_id = note_list.first_note_id(state['cache']['notes'])
        if note_id is not None:
            dispatch(select_note(note_id))

    return select_first


def select_next():
    def select_next(dispatch, state):
        note_id = note_list.next_note_id(
            state['cache']['notes'],
            state['ui_state']['current_note_id'])
        if note_id != state['ui_state']['current_note_id']:
            dispatch(select_note(note_id))

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        note_id = note_list.previous_note_id(
            state['cache']['notes'],
            state['ui_state']['current_note_id'])
        if note_id != state['ui_state']['current_note_id']:
            dispatch(select_note(note_id))

    return select_previous
