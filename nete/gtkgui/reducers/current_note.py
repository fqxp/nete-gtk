from nete.gtkgui.state.action_types import ActionType
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.SELECT_NOTE:
        return state.update({
            'id': action['id'],
            'note_title': action['title'],
            'note_text': action['text'],
            'needs_save': False,
        })

    elif action_type == ActionType.CREATE_NOTE:
        return state.update({
            'note_title': action['title'],
            'note_text': action['text'],
            'needs_save': True,
        })

    elif action_type == ActionType.CHANGE_NOTE_TEXT:
        return state.update({
            'note_text': action['text'],
            'needs_save': True,
        })

    elif action_type == ActionType.CHANGE_NOTE_TITLE:
        return state.update({
            'note_title': action['title'],
            'needs_save': True,
        })

    elif action_type == ActionType.NOTE_SAVED:
        return state.update({
            'needs_save': False,
        })

    else:
        return state
