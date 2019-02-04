from .action_types import ActionType
from .selection import select_note
from .editing import toggle_edit_note_title
from nete.gtkgui.state.utils import note_list
from nete.services.storage_factory import create_storage


def create_note():
    def create_note(dispatch, state):
        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        note = storage.create_note()

        dispatch(created_note(note))
        dispatch(select_note(note['title']))
        dispatch(toggle_edit_note_title())

    return create_note


def created_note(note):
    return {
        'type': ActionType.CREATED_NOTE,
        'note': note,
    }


def delete_note():
    def delete_note(dispatch, state):
        if state['current_note'] is None:
            return

        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        current_note_title = state['current_note']['title']
        next_note_title = (
            note_list.next_note_title(state['note_list']['notes'], current_note_title) or
            note_list.previous_note_title(state['note_list']['notes'], current_note_title)
        )
        dispatch(select_note(next_note_title))

        storage.delete(current_note_title)

        return {
            'type': ActionType.DELETE_NOTE,
            'note_title': current_note_title,
        }
    return delete_note


def save_note(note):
    def save_note(dispatch, state):
        if not note['needs_save']:
            return

        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        storage.save(note)
        dispatch(saved_note())

    return save_note


def saved_note():
    return {
        'type': ActionType.NOTE_SAVED,
    }


def load_notes(filter_term=None):
    def load_notes(dispatch, state):
        current_note_collection_id = state['ui']['current_note_collection_id']
        note_collection = state['note_collections'][current_note_collection_id]
        storage = create_storage(note_collection)
        dispatch(loaded_notes(storage.list()))

    return load_notes


def loaded_notes(notes):
    return {
        'type': ActionType.LOADED_NOTES,
        'notes': notes
    }
