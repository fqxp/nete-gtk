from nete.gui.actions.action_types import ActionType
from nete.gui.actions.selection import select_first
from nete.services import ui_state_storage


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
        return {
            'type': ActionType.LOADED_UI_STATE,
            'ui': ui_state,
        }

    return loaded_ui_state


def save_ui_state(ui_state):
    ui_state_storage.save_ui_state(ui_state)
