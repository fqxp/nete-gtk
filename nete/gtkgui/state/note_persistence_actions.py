from .actions import *
from nete.services.storage_factory import create_storage
from nete.gtkgui.state import note_list


def set_storage(storage_uri):
    return {
        'type': SET_STORAGE_URI,
        'storage_uri': storage_uri,
    }


def load_notes():
    def load_notes(dispatch, state):
        storage = create_storage(state['storage_uri'])
        dispatch(loaded_notes(
            note_list.build_entry(storage.load(note_id))
            for note_id in storage.list()
        ))

    return load_notes


def loaded_notes(notes):
    return {
        'type': LOADED_NOTES,
        'notes': notes
    }
