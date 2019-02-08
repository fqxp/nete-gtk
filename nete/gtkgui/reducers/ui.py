from fluous import create_reducer
from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.initial import Ui


reduce = create_reducer({
    ActionType.SELECT_NOTE: lambda state, action:
        state.update({
            'is_editing_title': False,
            'is_editing_text': False,
        }),

    ActionType.FOCUS_FILTER_TERM_ENTRY: lambda state, action: (
        state.update({
            'filter_term_entry_focus': True,
            'is_editing_title': False,
            'is_editing_text': False,
        }) if action['has_focus']
        else state.update({
            'filter_term_entry_focus': False,
        })
    ),

    ActionType.TOGGLE_EDIT_NOTE_TEXT: lambda state, action: (
        state.update({
            'is_editing_text': not state['is_editing_text'],
            'is_editing_title': False})),

    ActionType.TOGGLE_EDIT_NOTE_TITLE: lambda state, action: (
        state.update({
            'is_editing_title': not state['is_editing_title'],
            'is_editing_text': False})),

    ActionType.FINISH_EDIT_NOTE_TITLE: lambda state, action: (
        state.set('is_editing_title', False)),

    ActionType.CANCEL_EDIT_NOTE_TITLE: lambda state, action: (
        state.set('is_editing_title', False)),

    ActionType.FINISH_EDIT_NOTE_TEXT: lambda state, action: (
        state.set('is_editing_text', False)),

    ActionType.MOVE_PANED_POSITION: lambda state, action: (
        state.set('paned_position', action['position'])),

    ActionType.LOADED_UI_STATE: lambda state, action: (
        state.update(Ui.create(action['ui'])))
})
