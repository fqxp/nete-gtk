from .action_types import ActionType
from flurx import action


@action
def toggle_edit_mode_text():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TEXT,
    }


@action
def toggle_edit_mode_title():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TITLE,
    }


@action
def change_note_text(text):
    return {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'text': text,
    }


@action
def change_note_title(note_id, title):
    return {
        'type': ActionType.CHANGE_NOTE_TITLE,
        'id': note_id,
        'title': title,
    }


@action
def finish_edit_mode_text(note_id):
    return {
        'type': ActionType.FINISH_EDIT_NOTE_TEXT,
    }


@action
def finish_edit_mode_title():
    return {
        'type': ActionType.FINISH_EDIT_NOTE_TITLE,
    }


@action
def change_cursor_position(cursor_position):
    return {
        'type': ActionType.CHANGE_CURSOR_POSITION,
        'cursor_position': cursor_position,
    }
