from fluous import create_reducer
from nete.gui.actions.action_types import ActionType


reduce = create_reducer({
    ActionType.SELECT_NOTE: lambda state, action:
        (state.update(action['note'])
         if state and action['note']
         else action['note']
         ),

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
        }) if state else None,

    ActionType.NOTE_SAVED: lambda state, action:
        state.update({
            'needs_save': False,
        }),
})
