from nete.gtkgui.state.action_types import *
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff


def reduce(state, action):
    action_type = action['type']

    if action_type == SELECT_NOTE:
        return state.update({
            'note_title': action['title'],
            'note_text': action['text'],
        })

    elif action_type == CREATE_NOTE:
        return state.update({
            'note_title': action['title'],
            'note_text': action['text'],
        })

    elif action_type == CHANGE_NOTE_TEXT:
        return state.set('note_text', action['text'])

    elif action_type == CHANGE_NOTE_TITLE:
        return state \
            .set('note_title', action['title'])

    else:
        return state
