from nete.gtkgui.actions.action_types import ActionType


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.SELECT_NOTE:
        return state.update({
            'id': action['id'],
            'note_title': action['title'],
            'note_text': action['text'],
            'cursor_position': action['cursor_position'],
            'needs_save': False,
        })

    elif action_type == ActionType.CREATE_NOTE:
        return state.update({
            'id': action['note']['id'],
            'note_title': action['note']['title'],
            'note_text': action['note']['text'],
            'cursor_position': action['note']['cursor_position'],
            'needs_save': True,
        })

    elif action_type == ActionType.CHANGE_NOTE_TEXT:
        return state.update({
            'note_text': action['text'],
            'needs_save': True,
        })

    elif action_type == ActionType.CHANGE_CURSOR_POSITION:
        return state.update({
            'cursor_position': action['cursor_position'],
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
