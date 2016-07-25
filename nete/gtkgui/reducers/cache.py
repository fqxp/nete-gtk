from nete.gtkgui.state.action_types import ActionType
from nete.gtkgui.state.note_list import change_title, ordered, add_new
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.CREATE_NOTE:
        return state.set(
            'notes',
            add_new(state['notes'], action['note_id'], action['title']))

    elif action_type == ActionType.CHANGE_NOTE_TITLE:
        return state.set(
            'notes',
            ordered(change_title(state['notes'], action['note_id'], action['title'])))

    elif action_type == ActionType.LOADED_NOTES:
        return state.set('notes', ordered(action['notes']))

    else:
        return state
