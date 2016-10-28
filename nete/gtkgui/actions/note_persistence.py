from flurx import action
from nete.gtkgui.actions.action_types import ActionType
from nete.services.note_storage import create_storage


@action
def load_notes(filter_term=None):
    def load_notes(state):
        storage = create_storage(state['ui_state']['storage_uri'])
        loaded_notes(storage.list())

    return load_notes


@action
def loaded_notes(notes):
    return {
        'type': ActionType.LOADED_NOTES,
        'notes': notes
    }
