from .action_types import ActionType
from .selection import select_note, select_first
from nete.services import ui_state_storage


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


def save_ui_state(ui_state):
    ui_state_storage.save_ui_state(ui_state)
