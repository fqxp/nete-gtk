from .action_types import ActionType
from .selection import select_note
from nete.gtkgui.state import note_list
from nete.services.storage_factory import create_storage
import uuid


def create_note():
    return {
        'type': ActionType.CREATE_NOTE,
        'id': str(uuid.uuid4()),
        'title': 'New Note',
        'text': '',
    }


def delete_note():
    def delete_note(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        current_note_id = state['ui_state']['current_note_id']
        next_note_id = (
            note_list.next_note_id(state['cache']['notes'], current_note_id) or
            note_list.previous_note_id(state['cache']['notes'], current_note_id)
        )
        dispatch(select_note(next_note_id))

        storage.delete(current_note_id)
        return {
            'type': ActionType.DELETE_NOTE,
            'note_id': current_note_id,
        }
    return delete_note


def save_note(note):
    def save_note(dispatch, state):
        if not note['needs_save']:
            return

        storage = create_storage(note['storage_uri'])
        storage.save(note)
        dispatch(saved_note())

    return save_note


def saved_note():
    return {
        'type': ActionType.NOTE_SAVED,
    }


def load_notes(filter_term=None):
    def load_notes(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        dispatch(loaded_notes(storage.list()))

    return load_notes


def loaded_notes(notes):
    return {
        'type': ActionType.LOADED_NOTES,
        'notes': notes
    }
