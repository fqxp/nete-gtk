from .action_types import *
from nete.services.storage_factory import create_storage
import uuid


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


def create_note():
    return {
        'type': CREATE_NOTE,
        'note_id': str(uuid.uuid4()),
        'title': 'New Note',
        'text': '',
    }


def select_first():
    return {
        'type': SELECT_FIRST,
    }


def select_next():
    return {
        'type': SELECT_NEXT,
    }


def select_previous():
    return {
        'type': SELECT_PREVIOUS,
    }

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


def move_or_resize_window(x, y, width, height):
    return {
        'type': MOVE_OR_RESIZE_WINDOW,
        'position': [x, y],
        'size': [width, height],
    }


def loaded_ui_state(ui_state):
    return {
        'type': LOADED_UI_STATE,
        'ui_state': ui_state,
    }
