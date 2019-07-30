from fluous import create_reducer
from pyrsistent import ny

from nete.gui.actions.action_types import ActionType
from nete.gui.state.utils.note_list import (
    add_new,
    is_visible,
    ordered,
    without
)
from nete.gui.state.models import NoteListItem


reduce = create_reducer({
    ActionType.CANCEL_EDIT_NOTE_TITLE: lambda state, action: (
        state.transform(['ui', 'focus'], 'note_view')),

    ActionType.CHANGE_CURSOR_POSITION: lambda state, action:
        state.transform(
            ['current_note', 'cursor_position'], action['cursor_position']
        ) if state['current_note'] else state,

    ActionType.CHANGE_FILTER_TERM: lambda state, action:
        state.transform(
            ['note_list', 'notes', ny], (
                lambda note: note.set('visible',
                                      is_visible(note['title'],
                                                 action['filter_term']))),
            ['note_list', 'filter_term'], action['filter_term'],
            ['note_list', 'preselected_note_title'], (
                preselected_note(state['note_list'], action['filter_term']))),

    ActionType.CHANGE_NOTE_TEXT: lambda state, action:
        state.transform(
            ['current_note', 'text'], action['text'],
            ['current_note', 'needs_save'], True
        ) if state['current_note'] else state,

    ActionType.CLOSE_NOTE: lambda state, action:
        state.transform(['current_note'], None),

    ActionType.CREATED_NOTE: lambda state, action:
        state.transform(
            ['note_list', 'notes'], add_new(
                state['note_list']['notes'],
                NoteListItem(
                    title=action['note']['title'],
                    visible=is_visible(action['note']['title'],
                                       state['note_list']['filter_term'])))
        ),

    ActionType.DELETE_NOTE: lambda state, action:
        state.transform(
            ['note_list', 'notes'], (
                without(state['note_list']['notes'], action['note_title']))
        ),

    ActionType.FINISH_EDIT_NOTE_TEXT: lambda state, action: (
        state.transform(['ui', 'focus'], 'note_view')),

    ActionType.FINISH_EDIT_NOTE_TITLE: lambda state, action:
        state.transform(
            ['current_note'], (
                lambda note: note.set(
                    'title',
                    action['new_title']) if note else note
            ),
            ['ui', 'focus'], 'note_view',
            ['note_list', 'notes', ny, 'title'], (
                lambda title: action['new_title']
                if title == action['old_title']
                else title
            ),
            ['note_list', 'notes', ny], (
                lambda note_list_item: note_list_item.set(
                    'visible',
                    is_visible(note_list_item['title'],
                               state['note_list']['filter_term']))
            ),
        ),

    ActionType.FOCUS: lambda state, action:
        state.transform(
            ['ui', 'focus'], action['widget_name'],
        ),

    # ActionType.FOCUS_FILTER_TERM_ENTRY: lambda state, action:
    #     state.transform(
    #         ['ui', 'focus'], 'filter_term_entry',
    #         ['note_list', 'preselected_note_title'], (
    #             first_visible_note(
    #                 state['note_list']['notes'],
    #                 state['note_list']['filter_term']))
    #     ),

    ActionType.LOAD_CONFIGURATION: lambda state, action:
        state.transform(
            ['configuration'], action['configuration'],
            ['ui', 'current_note_collection_id'], (
                list(action['configuration'].note_collections)[0].id)
        ),

    ActionType.LOADED_UI_STATE: lambda state, action:
        state.transform(['ui'], lambda c: c.update(action['ui'])),

    ActionType.MOVE_PANED_POSITION: lambda state, action: (
        state.transform(['ui', 'paned_position'], action['position'])),

    ActionType.NOTE_SAVED: lambda state, action:
        state.transform(
            ['current_note', 'needs_save'], False
        ) if state['current_note'] else state,

    ActionType.PRESELECT_NOTE: lambda state, action:
        state.transform(
            ['note_list', 'preselected_note_title'], action['note_title']
        ),

    ActionType.RESET: lambda state, action:
        state.transform(
            ['ui', 'focus'], 'note_view',
            ['note_list', 'preselected_note_title'], None,
        ),

    ActionType.SELECT_NOTE: lambda state, action:
        state.transform(
            ['current_note'], action['note'],
            ['ui', 'focus'], 'note_view',
            ['note_list', 'preselected_note_title'], None,
        ),

    ActionType.SELECT_NOTE_COLLECTION: lambda state, action:
        state.transform(
            ['current_note'], None,
            ['ui', 'current_note_collection_id'], action['collection_id'],
            ['ui', 'focus'], 'filter_term_entry',
            ['note_list', 'preselected_note_title'], None,
            ['note_list', 'notes'], ordered(action['notes']),
            ['ui', 'focus'], 'filter_term_entry',
        ),

    ActionType.TOGGLE_EDIT_NOTE_TEXT: lambda state, action:
        state.transform(
            ['ui', 'focus'], (
                'note_editor' if state['ui']['focus'] != 'note_editor'
                else 'note_view')
        ) if state['current_note'] is not None else state,

    ActionType.TOGGLE_EDIT_NOTE_TITLE: lambda state, action:
        state.transform(
            ['ui', 'focus'], (
                'note_title_editor' if state['ui']['focus'] != 'note_title_editor'
                else 'note_view')
        ) if state['current_note'] is not None else state,
})


def first_visible_note(notes, filter_term):
    return next(
        (note['title']
         for note in notes
         if is_visible(note['title'], filter_term)),
        None)


def preselected_note(state, filter_term):
    return (
        first_visible_note(state['notes'], filter_term)
        if not state['preselected_note_title']
        else (
            state['preselected_note_title']
            if is_visible(
                state['preselected_note_title'],
                filter_term)
            else first_visible_note(state['notes'], filter_term)))
