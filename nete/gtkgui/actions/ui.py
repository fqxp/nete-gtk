from .action_types import ActionType
from .selection import select_first, load_note
from nete.services import ui_state_storage
from flurx import action


@action
def move_paned(new_position):
    return {
        'type': ActionType.MOVE_PANED_POSITION,
        'position': new_position,
    }


@action
def load_ui_state():
    def load_ui_state(state):
        try:
            ui_state = ui_state_storage.load_ui_state()
            loaded_ui_state(ui_state)
        except FileNotFoundError:
            select_first()

    return load_ui_state


@action
def loaded_ui_state(ui_state):
    def loaded_ui_state(state):
        if ui_state['current_note_id']:
            load_note(ui_state['current_note_id'])

        return {
            'type': ActionType.LOADED_UI_STATE,
            'ui_state': ui_state,
        }

    return loaded_ui_state


@action
def quit():
    return {}
