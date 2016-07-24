from nete.gtkgui.state.action_types import *
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff
from immutable.functions import make_immutable


@log_state_diff
def reduce(state, action):
    action_type = action['type']

    if action_type == SELECT_NOTE:
        return state.update({
            'current_note_id': action['note_id'],
            'is_editing_title': False,
            'is_editing_text': False,
        })

    elif action_type == CREATE_NOTE:
        return state.update({
            'current_note_id': action['note_id'],
            'is_editing_title': True,
            'is_editing_text': False,
        })

    elif action_type == TOGGLE_EDIT_NOTE_TEXT:
        return state \
            .set('is_editing_text', not state['is_editing_text']) \
            .set('is_editing_title', False)

    elif action_type == TOGGLE_EDIT_NOTE_TITLE:
        return state \
            .set('is_editing_title', not state['is_editing_title']) \
            .set('is_editing_text', False)

    elif action_type == FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)

    elif action_type == FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)

    elif action_type == MOVE_OR_RESIZE_WINDOW:
        return state \
            .set('window_position', action['position']) \
            .set('window_size', action['size'])

    elif action_type == MOVE_PANED_POSITION:
        return state \
            .set('paned_position', action['position'])

    elif action_type == LOADED_UI_STATE:
        new_ui_state = dict(state)
        new_ui_state.update(action['ui_state'])
        return make_immutable(new_ui_state)

    else:
        return state
