from .action_types import *
from nete.services.storage_factory import create_storage


def select_note(note_id):
    def load_note(dispatch, state):
        storage = create_storage(state['storage_uri'])
        note = storage.load(note_id)

        return {
            'type': SELECT_NOTE,
            'note_id': note['id'],
            'title': note['title'],
            'text': note['text'],
        }

    return load_note


def toggle_edit_note_text():
    return {
        'type': TOGGLE_EDIT_NOTE_TEXT,
    }


def change_note_text(note_id, text):
    return {
        'type': CHANGE_NOTE_TEXT,
        'note_id': note_id,
        'text': text,
    }


def finish_edit_note_text(note_id):
    return {
        'type': FINISH_EDIT_NOTE_TEXT,
    }


def toggle_edit_note_title():
    return {
        'type': TOGGLE_EDIT_NOTE_TITLE,
    }


def change_note_title(note_id, title):
    return {
        'type': CHANGE_NOTE_TITLE,
        'note_id': note_id,
        'title': title,
    }


def finish_edit_note_title():
    return {
        'type': FINISH_EDIT_NOTE_TITLE,
    }


def loaded_notes(notes):
    return {
        'type': LOADED_NOTES,
        'notes': notes
    }
