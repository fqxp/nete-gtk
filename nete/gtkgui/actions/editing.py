from nete.services.storage_factory import create_storage
from .action_types import ActionType


def toggle_edit_note_text():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TEXT,
    }


def change_note_text(text):
    return {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'text': text,
    }


def change_cursor_position(cursor_position):
    return {
        'type': ActionType.CHANGE_CURSOR_POSITION,
        'cursor_position': cursor_position,
    }


def finish_edit_note_text(note_id):
    return {
        'type': ActionType.FINISH_EDIT_NOTE_TEXT,
    }


def toggle_edit_note_title():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TITLE,
    }



def finish_edit_note_title(new_title):
    def finish_edit_note_title(dispatch, state):
        old_title = state['current_note']['title']
        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        storage.move(old_title, new_title)

        return {
            'type': ActionType.FINISH_EDIT_NOTE_TITLE,
            'old_title': old_title,
            'new_title': new_title,
        }

    return finish_edit_note_title


def cancel_edit_note_title():
    return {
        'type': ActionType.CANCEL_EDIT_NOTE_TITLE,
    }
