from .action_types import ActionType
from nete.services.storage_factory import create_storage
from nete.gtkgui.state import note_list


def select_note(note_id):
    if note_id is None:
        return

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
        first_note_id = note_list.first_note_id(state['cache']['notes'])
        if first_note_id is not None:
            return select_note(first_note_id)

    return select_first


def select_last():
    def select_last(dispatch, state):
        last_note_id = note_list.last_note_id(state['cache']['notes'])
        if last_note_id is not None:
            return select_note(last_note_id)

    return select_last


def select_next():
    def select_next(dispatch, state):
        notes = state['cache']['notes']
        current_note_id = state['ui_state']['current_note_id']

        if not note_list.contains(notes, current_note_id):
            return select_first()

        next_note_id = note_list.next_note_id(notes, current_note_id)
        if next_note_id:
            return select_note(next_note_id)

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        notes = state['cache']['notes']
        current_note_id = state['ui_state']['current_note_id']

        if not note_list.contains(notes, current_note_id):
            return select_last()

        previous_note_id = note_list.previous_note_id(notes, current_note_id)
        if previous_note_id is not None:
            return select_note(previous_note_id)

    return select_previous
