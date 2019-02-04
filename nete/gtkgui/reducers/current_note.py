from nete.gtkgui.actions.action_types import ActionType


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.SELECT_NOTE:
        if state is None:
            return action['note']
        else:
            return state.update(action['note'])

    elif action_type == ActionType.CHANGE_NOTE_TEXT:
        return state.update({
            'text': action['text'],
            'needs_save': True,
        })

    elif action_type == ActionType.FINISH_EDIT_NOTE_TITLE:
        return state.update({
            'title': action['new_title'],
        })

    elif action_type == ActionType.CHANGE_CURSOR_POSITION:
        return state.update({
            'cursor_position': action['cursor_position'],
        })

    elif action_type == ActionType.NOTE_SAVED:
        return state.update({
            'needs_save': False,
        })

    else:
        return state
