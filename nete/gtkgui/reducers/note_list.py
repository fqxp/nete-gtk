from nete.gtkgui.actions.action_types import ActionType
from nete.gtkgui.state.utils.note_list import change_title, ordered, add_new, is_visible, without
from nete.gtkgui.state.models import NoteListItem


def reduce(state, action):
    action_type = action['type']

    if action_type == ActionType.CREATED_NOTE:
        note_list_item = NoteListItem(
            title=action['note']['title'],
            visible=False
            )
        note_list_item = note_list_item.set(
            'visible',
            is_visible(note_list_item['title'], state['filter_term']))

        return state.set('notes', add_new(state['notes'], note_list_item))

    elif action_type == ActionType.DELETE_NOTE:
        return state.set(
            'notes', without(state['notes'], action['note_title']))

    elif action_type == ActionType.FINISH_EDIT_NOTE_TITLE:
        return state.set(
            'notes',
            ordered(
                change_title(state['notes'],
                             action['old_title'],
                             action['new_title'])))

    elif action_type == ActionType.CHANGE_FILTER_TERM:
        return (state
                .set('notes', [
                    note.set('visible', is_visible(note['title'],
                                                   action['filter_term']))
                    for note in state['notes']
                ])
                .set('filter_term', action['filter_term']))

    elif action_type == ActionType.LOADED_NOTES:
        return state.set('notes', ordered(action['notes']))

    elif action_type == ActionType.CHANGE_FILTER_TERM:
        return state.update({
            'filter_term': action['filter_term'],
        })

    else:
        return state
