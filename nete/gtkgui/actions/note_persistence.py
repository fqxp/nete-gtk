from .action_types import ActionType
from nete.gtkgui.state import note_list
from nete.services.storage_factory import create_storage
import uuid


def create_note():
    return {
        'type': ActionType.CREATE_NOTE,
        'note_id': str(uuid.uuid4()),
        'title': 'New Note',
        'text': '',
    }


def saved_note():
    return {
        'type': ActionType.NOTE_SAVED,
    }


def load_notes():
    def load_notes(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        dispatch(loaded_notes(
            note_list.build_entry(storage.load(note_id))
            for note_id in storage.list()
        ))

    return load_notes


def loaded_notes(notes):
    return {
        'type': ActionType.LOADED_NOTES,
        'notes': notes
    }
