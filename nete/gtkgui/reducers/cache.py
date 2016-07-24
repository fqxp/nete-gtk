from nete.gtkgui.state.action_types import *
from nete.gtkgui.state import note_list
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff


def reduce(state, action):
    action_type = action['type']

    if action_type == CREATE_NOTE:
        return state.update({
            'notes': note_list.add_new(
                state['notes'], action['note_id'], action['title'])
        })

    elif action_type == CHANGE_NOTE_TITLE:
        return state \
            .set('notes',
                 note_list.ordered(
                    note_list.change_title(state['notes'], action['note_id'], action['title'])))

    elif action_type == LOADED_NOTES:
        return state.set('notes', note_list.ordered(action['notes']))

    else:
        return state
