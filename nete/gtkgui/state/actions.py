from .action_types import ActionType
from nete.services.storage_factory import create_storage
from nete.services import ui_state_storage
from nete.gtkgui.state import note_list
import uuid


def select_note(note_id):
    def load_note(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        note = storage.load(note_id)

        dispatch({
            'type': ActionType.SELECT_NOTE,
            'note_id': note['id'],
            'title': note['title'],
            'text': note['text'],
        })

    return load_note


def create_note():
    return {
        'type': ActionType.CREATE_NOTE,
        'note_id': str(uuid.uuid4()),
        'title': 'New Note',
        'text': '',
    }


def select_first():
    def select_first(dispatch, state):
        note_id = note_list.first_note_id(state['cache']['notes'])
        if note_id is not None:
            dispatch(select_note(note_id))

    return select_first


def select_next():
    def select_next(dispatch, state):
        note_id = note_list.next_note_id(
            state['cache']['notes'],
            state['ui_state']['current_note_id'])
        if note_id != state['ui_state']['current_note_id']:
            dispatch(select_note(note_id))

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        note_id = note_list.previous_note_id(
            state['cache']['notes'],
            state['ui_state']['current_note_id'])
        if note_id != state['ui_state']['current_note_id']:
            dispatch(select_note(note_id))

    return select_previous


def toggle_edit_note_text():
    return {
        'type': TOGGLE_EDIT_NOTE_TEXT,
    }


def change_note_text(note_id, text):
    return {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'note_id': note_id,
        'text': text,
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


def move_or_resize_window(x, y, width, height):
    return {
        'type': ActionType.MOVE_OR_RESIZE_WINDOW,
        'position': [x, y],
        'size': [width, height],
    }


def move_paned_position(position):
    return {
        'type': ActionType.MOVE_PANED_POSITION,
        'position': position,
    }


def load_ui_state():
    def load_ui_state(dispatch, state):
        try:
            ui_state = ui_state_storage.load_ui_state()
            dispatch(loaded_ui_state(ui_state))
        except FileNotFoundError:
            dispatch(select_first())

    return load_ui_state


def loaded_ui_state(ui_state):
    def loaded_ui_state(dispatch, state):
        if ui_state['current_note_id'] is not None:
            dispatch(select_note(ui_state['current_note_id']))

        return {
            'type': ActionType.LOADED_UI_STATE,
            'ui_state': ui_state,
        }

    return loaded_ui_state
