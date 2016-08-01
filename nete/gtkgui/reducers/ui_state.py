from nete.gtkgui.actions.action_types import ActionType
from pyrsistent import freeze, thaw


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.SELECT_NOTE:
        return state.update({
            'current_note_id': action['id'],
            'is_editing_title': False,
            'is_editing_text': False,
        })

    elif action_type == ActionType.CREATE_NOTE:
        return state.update({
            'current_note_id': action['id'],
            'is_editing_title': True,
            'is_editing_text': False,
        })

    elif action_type == ActionType.TOGGLE_EDIT_NOTE_TEXT:
        return state.update({
            'is_editing_text': not state['is_editing_text'],
            'is_editing_title': False})

    elif action_type == ActionType.TOGGLE_EDIT_NOTE_TITLE:
        return state.update({
            'is_editing_title': not state['is_editing_title'],
            'is_editing_text': False})

    elif action_type == ActionType.FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)

    elif action_type == ActionType.FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)

    elif action_type == ActionType.MOVE_OR_RESIZE_WINDOW:
        return state.update({
            'window_position': freeze(action['position']),
            'window_size': freeze(action['size'])
        })

    elif action_type == ActionType.MOVE_PANED_POSITION:
        return state.set('paned_position', action['position'])

    elif action_type == ActionType.LOADED_UI_STATE:
        return state.update(freeze(action['ui_state']))

    else:
        return state
