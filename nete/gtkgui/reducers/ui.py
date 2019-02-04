from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.initial import Ui


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.SELECT_NOTE:
        return state.update({
            'is_editing_title': False,
            'is_editing_text': False,
        })

    elif action_type == ActionType.FOCUS_FILTER_TERM_ENTRY:
        if action['has_focus']:
            return state.update({
                'filter_term_entry_focus': True,
                'is_editing_title': False,
                'is_editing_text': False,
            })
        else:
            return state.update({
                'filter_term_entry_focus': False,
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

    elif action_type == ActionType.CANCEL_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)

    elif action_type == ActionType.FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)

    elif action_type == ActionType.MOVE_PANED_POSITION:
        return state.set('paned_position', action['position'])

    elif action_type == ActionType.LOADED_UI_STATE:
        return state.update(Ui.create(action['ui']))

    else:
        return state
