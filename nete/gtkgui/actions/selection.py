from .action_types import ActionType
from nete.services.storage_factory import create_storage
from nete.gtkgui.state.utils import note_list


def select_note(note_title):
    if note_title is None:
        return

    def load_note(dispatch, state):
        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        note = storage.load(note_title)

        dispatch({
            'type': ActionType.SELECT_NOTE,
            'note': note,
        })

    return load_note


def select_first():
    def select_first(dispatch, state):
        first_note_title = note_list.first_note_title(state['note_list']['notes'])
        if first_note_title is None:
            return

        return select_note(first_note_title)

    return select_first


def select_last():
    def select_last(dispatch, state):
        last_note_title = note_list.last_note_title(state['note_list']['notes'])
        if last_note_title is None:
            return

        return select_note(last_note_title)

    return select_last


def select_next():
    def select_next(dispatch, state):
        if state['current_note'] is None:
            return select_first()

        notes = state['note_list']['notes']
        current_note_title = state['current_note']['title']

        if not note_list.contains(notes, current_note_title):
            return select_first()

        next_note_title = note_list.next_note_title(notes, current_note_title)
        if next_note_title:
            return select_note(next_note_title)

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        if state['current_note'] is None:
            return select_last()

        notes = state['note_list']['notes']
        current_note_title = state['current_note']['title']

        if not note_list.contains(notes, current_note_title):
            return select_last()

        previous_note_title = note_list.previous_note_title(notes, current_note_title)
        if previous_note_title is not None:
            return select_note(previous_note_title)

    return select_previous
