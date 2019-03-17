from fluous import create_reducer
from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.initial import Ui


reduce = create_reducer({
    ActionType.SELECT_NOTE: lambda state, action: (
        state.set('focus', 'note_view')),

    ActionType.FOCUS_FILTER_TERM_ENTRY: lambda state, action: (
        state.set('focus', 'filter_term')),

    ActionType.TOGGLE_EDIT_NOTE_TEXT: lambda state, action: (
        state.set('focus',
                  'note_editor'
                  if state['focus'] != 'note_editor'
                  else 'note_view')),

    ActionType.TOGGLE_EDIT_NOTE_TITLE: lambda state, action: (
        state.set('focus',
                  'note_title_editor'
                  if state['focus'] != 'note_title_editor'
                  else 'note_view')),

    ActionType.FINISH_EDIT_NOTE_TITLE: lambda state, action: (
        state.set('focus', 'note_view')),

    ActionType.CANCEL_EDIT_NOTE_TITLE: lambda state, action: (
        state.set('focus', 'note_view')),

    ActionType.FINISH_EDIT_NOTE_TEXT: lambda state, action: (
        state.set('focus', 'note_view')),

    ActionType.MOVE_PANED_POSITION: lambda state, action: (
        state.set('paned_position', action['position'])),

    ActionType.LOADED_UI_STATE: lambda state, action: (
        state.update(Ui.create(action['ui'])))
})
