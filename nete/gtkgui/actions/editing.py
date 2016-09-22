from .action_types import ActionType


def toggle_edit_note_text():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TEXT,
    }


def change_note_text(note_id, text):
    return {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'note_id': note_id,
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


def change_note_title(note_id, title):
    return {
        'type': ActionType.CHANGE_NOTE_TITLE,
        'note_id': note_id,
        'title': title,
    }


def finish_edit_note_title():
    return {
        'type': ActionType.FINISH_EDIT_NOTE_TITLE,
    }
