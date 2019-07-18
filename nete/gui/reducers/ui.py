from fluous import create_reducer
from nete.gui.actions.action_types import ActionType
from nete.gui.state.initial import Ui


reduce = create_reducer({
    ActionType.SELECT_NOTE_COLLECTION: lambda state, action: (
        state.set('current_note_collection_id', action['collection_id'])),

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
        state.update(Ui.create(action['ui']))),

    ActionType.LOAD_CONFIGURATION: lambda state, action: (
        state.set(
            'current_note_collection_id',
            list(action['configuration'].note_collections)[0].id
        )),
})
