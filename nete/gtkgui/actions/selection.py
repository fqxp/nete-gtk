from .action_types import ActionType
from nete.services.storage_factory import create_storage
from nete.gtkgui.state.selectors import (
    current_note,
    note_list_contains,
    note_list_first,
    note_list_last,
    note_list_next,
    note_list_previous,
    visible_notes)


def load_note(note_title):
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
        first_note_title = note_list_first(state)['title']

        if first_note_title is None:
            return

        return load_note(first_note_title)

    return select_first


def select_last():
    def select_last(dispatch, state):
        last_note_title = note_list_last(state)
        if last_note_title is None:
            return

        return load_note(last_note_title)

    return select_last


def select_next():
    def select_next(dispatch, state):
        note = current_note(state)
        if note is None:
            return select_first()

        current_note_title = note['title']

        if not note_list_contains(state, current_note_title):
            return select_first()

        next_note_title = note_list_next(state, current_note_title)
        if next_note_title:
            return load_note(next_note_title)

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        note = current_note(state)
        if note is None:
            return select_last()

        current_note_title = note['title']

        if not note_list_contains(state, current_note_title):
            return select_last()

        previous_note_title = note_list_previous(state, current_note_title)
        if previous_note_title is not None:
            return load_note(previous_note_title)

    return select_previous


def preselect_note(title):
    return {
        'type': ActionType.PRESELECT_NOTE,
        'note_title': title,
    }


def preselect_next():
    def preselect_next(dispatch, state):
        if len(state['note_list']['notes']) is None:
            return

        preselected_note_title = state['note_list']['preselected_note_title']
        if preselected_note_title is None:
            return preselect_note(visible_notes(state)[0]['title'])

        next_note_title = note_list_next(state, preselected_note_title)
        if next_note_title is not None:
            return preselect_note(next_note_title)

    return preselect_next


def preselect_previous():
    def preselect_previous(dispatch, state):
        if len(state['note_list']['notes']) is None:
            return

        preselected_note_title = state['note_list']['preselected_note_title']
        if preselected_note_title is None:
            return preselect_note(visible_notes(state)[-1]['title'])

        previous_note_title = note_list_previous(state, preselected_note_title)
        if previous_note_title is not None:
            return preselect_note(previous_note_title)

    return preselect_previous


def choose_preselected_note():
    def choose_preselected_note(dispatch, state):
        preselected_note_title = state['note_list']['preselected_note_title']

        if preselected_note_title is None:
            return

        return load_note(preselected_note_title)

    return choose_preselected_note
