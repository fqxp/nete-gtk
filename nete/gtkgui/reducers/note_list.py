from fluous import create_reducer
from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.utils.note_list import change_title, ordered, add_new, is_visible, without
from nete.gtkgui.state.models import NoteListItem


def created_note(state, action):
    note_list_item = NoteListItem(
        title=action['note']['title'],
        visible=False)
    note_list_item = note_list_item.set(
        'visible',
        is_visible(note_list_item['title'], state['filter_term']))

    return state.set('notes', add_new(state['notes'], note_list_item))


reduce = create_reducer({
    ActionType.CREATED_NOTE: created_note,

    ActionType.DELETE_NOTE: lambda state, action:
        state.set('notes',
                  without(state['notes'], action['note_title'])),

    ActionType.FINISH_EDIT_NOTE_TITLE: lambda state, action:
        state.set('notes',
                  ordered(
                      change_title(state['notes'],
                                   action['old_title'],
                                   action['new_title']))),

    ActionType.CHANGE_FILTER_TERM: lambda state, action: (
        state
        .set('notes', [
            note.set('visible',
                     is_visible(note['title'], action['filter_term']))
            for note in state['notes']])
        .set('filter_term', action['filter_term'])),

    ActionType.LOADED_NOTES: lambda state, action: (
        state.set('notes', ordered(action['notes']))),
})
