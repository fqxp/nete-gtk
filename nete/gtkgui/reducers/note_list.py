from fluous import create_reducer
from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.utils.note_list import change_title, ordered, add_new, is_visible, without
from nete.gtkgui.state.models import NoteListItem
from functools import lru_cache


def created_note(state, action):
    note_list_item = NoteListItem(
        title=action['note']['title'],
        visible=False)
    note_list_item = note_list_item.set(
        'visible',
        is_visible(note_list_item['title'], state['filter_term']))

    return state.set('notes', add_new(state['notes'], note_list_item))


def first_visible_note(state):
    return next(
        (note['title']
         for note in state['notes']
         if is_visible(note['title'], state['filter_term'])),
        None)


reduce = create_reducer({
    ActionType.SELECT_NOTE: lambda state, action:
        state.set('preselected_note_title', None),

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

    ActionType.FOCUS_FILTER_TERM_ENTRY: lambda state, action: (
        state.set('preselected_note_title',
                  first_visible_note(state))),

    ActionType.CHANGE_FILTER_TERM: lambda state, action: (
        state
        .set('notes', [
            note.set('visible',
                     is_visible(note['title'], action['filter_term']))
            for note in state['notes']])
        .set('filter_term', action['filter_term'])
        .set('preselected_note_title', (
            first_visible_note(state)
            if not state['preselected_note_title']
            else (
                state['preselected_note_title']
                if is_visible(state['preselected_note_title'], action['filter_term'])
                else first_visible_note(state))))),

    ActionType.LOADED_NOTES: lambda state, action: (
        state.set('notes', ordered(action['notes']))),

    ActionType.PRESELECT_NOTE: lambda state, action: (
        state.set('preselected_note_title', action['note_title'])),
})
