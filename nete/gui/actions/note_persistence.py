from nete.gui.actions.action_types import ActionType
from nete.gui.actions.selection import select_note
from nete.gui.actions.editing import toggle_edit_note_title
from nete.gui.state.selectors import (
    current_note,
    current_note_collection,
    note_list_next,
    note_list_previous,
)
from nete.services.storage_factory import create_storage


def create_note():
    def create_note(dispatch, state):
        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        note = storage.create_note()

        dispatch(created_note(note))
        dispatch(select_note(note['title']))
        dispatch(toggle_edit_note_title())

    return create_note


def created_note(note):
    return {
        'type': ActionType.CREATED_NOTE,
        'note': note,
    }


def delete_note():
    def delete_note(dispatch, state):
        if current_note(state) is None:
            return

        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        current_note_title = current_note(state)['title']
        next_note_title = (
            note_list_next(state, current_note_title)
            or note_list_previous(state, current_note_title)
        )
        dispatch(select_note(next_note_title))

        storage.delete(current_note_title)

        return {
            'type': ActionType.DELETE_NOTE,
            'note_title': current_note_title,
        }
    return delete_note


def save_note(note):
    def save_note(dispatch, state):
        if note is None or not note['needs_save']:
            return

        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        storage.save(note)
        dispatch(saved_note())

    return save_note


def saved_note():
    return {
        'type': ActionType.NOTE_SAVED,
    }
