from nete.gui.actions.action_types import ActionType
from nete.gui.actions.selection import select_first
from nete.gui.state.selectors import (
    current_note_collection,
    note_collection_by_id,
)
from nete.services import ui_state_storage
from nete.services.storage_factory import create_storage


def move_paned_position(position):
    return {
        'type': ActionType.MOVE_PANED_POSITION,
        'position': position,
    }


def focus_note_collection_chooser():
    return {
        'type': ActionType.FOCUS_NOTE_COLLECTION_CHOOSER,
    }


def initialize():
    def initialize(dispatch, state):
        note_collection = current_note_collection(state)
        dispatch(select_collection(note_collection.id))
    return initialize


def reset():
    return {
        'type': ActionType.RESET,
    }


def select_collection(collection_id):
    def select_collection(dispatch, state):
        note_collection = note_collection_by_id(state, collection_id)
        storage = create_storage(note_collection)
        dispatch({
            'type': ActionType.SELECT_NOTE_COLLECTION,
            'collection_id': collection_id,
            'notes': storage.list(),
        })
    return select_collection


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
        return {
            'type': ActionType.LOADED_UI_STATE,
            'ui': ui_state,
        }

    return loaded_ui_state


def save_ui_state(ui_state):
    ui_state_storage.save_ui_state(ui_state)
