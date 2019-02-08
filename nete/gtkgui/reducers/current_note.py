from fluous import create_reducer
from nete.gtkgui.actions.action_types import ActionType


reduce = create_reducer({
    ActionType.SELECT_NOTE: lambda state, action:
        action['note'] if state is None else state.update(action['note']),

    ActionType.CHANGE_NOTE_TEXT: lambda state, action:
        state.update({
            'text': action['text'],
            'needs_save': True,
        }),

    ActionType.FINISH_EDIT_NOTE_TITLE: lambda state, action:
        state.update({
            'title': action['new_title'],
        }),

    ActionType.CHANGE_CURSOR_POSITION: lambda state, action:
        state.update({
            'cursor_position': action['cursor_position'],
        }),

    ActionType.NOTE_SAVED: lambda state, action:
        state.update({
            'needs_save': False,
        }),
})
