from fluous.store import Store
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff
from gi.repository import Gtk
from nete.services.storage_factory import create_storage
from nete.services.note_persistence import NotePersistence
from nete.gtkgui.main_window import ConnectedMainWindow
from nete.gtkgui.state.action_types import *
from nete.gtkgui.state.actions import loaded_notes, select_first, select_note
from nete.gtkgui.state import note_list


initial_state = {
    'storage_uri': 'nete:notes',
    'current_note_id': None,
    'is_editing_title': False,
    'is_editing_text': False,
    'note_title': None,
    'note_text': None,
    'notes': [],
}


# @log_traceback
@log_state_diff
@log_action
def reducer(state, action):
    action_type = action['type']

    if action_type == SELECT_NOTE:
        return state.update({
            'current_note_id': action['note_id'],
            'note_title': action['title'],
            'note_text': action['text'],
            'is_editing_title': False,
            'is_editing_text': False,
        })
    elif action_type == CREATE_NOTE:
        return state.update({
            'current_note_id': action['note_id'],
            'note_title': action['title'],
            'note_text': action['text'],
            'is_editing_title': True,
            'is_editing_text': False,
            'notes': note_list.add_new(
                state['notes'], action['note_id'], action['title'])})
    elif action_type == CHANGE_NOTE_TEXT:
        return state.set('note_text', action['text'])
    elif action_type == CHANGE_NOTE_TITLE:
        return state \
            .set('note_title', action['title']) \
            .set('notes',
                 note_list.ordered(
                    note_list.change_title(state['notes'], action['note_id'], action['title'])))
    elif action_type == TOGGLE_EDIT_NOTE_TEXT:
        return state \
            .set('is_editing_text', not state['is_editing_text']) \
            .set('is_editing_title', False)
    elif action_type == TOGGLE_EDIT_NOTE_TITLE:
        return state \
            .set('is_editing_title', not state['is_editing_title']) \
            .set('is_editing_text', False)
    elif action_type == FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)
    elif action_type == FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)
    elif action_type == LOADED_NOTES:
        return state.set('notes', note_list.ordered(action['notes']))
    else:
        return state


def relative_selection_middleware(state, action):
    action_type = action['type']

    if action_type == SELECT_FIRST:
        note_id = note_list.first_note_id(state['notes'])
        return select_note(note_id)
    elif action_type == SELECT_NEXT:
        note_id = note_list.next_note_id(
            state['notes'],
            state['current_note_id'])
        return select_note(note_id)
    elif action_type == SELECT_PREVIOUS:
        note_id = note_list.previous_note_id(
            state['notes'],
            state['current_note_id'])
        return select_note(note_id)
    else:
        return action


class Application:

    def __init__(self):
        store = Store(reducer, initial_state)
        store.add_middleware(relative_selection_middleware)
        self.persistence = NotePersistence(store)

        self.load_notes(store, store.state['storage_uri'])

        self.main_window = ConnectedMainWindow(store)
        self.main_window.connect("delete-event", Gtk.main_quit)

        store.dispatch(select_first())

    def show_window(self):
        self.main_window.show_all()

    def load_notes(self, store, storage_uri):
        storage = create_storage(storage_uri)
        store.dispatch(loaded_notes(
            note_list.build_entry(storage.load(note_id))
            for note_id in storage.list()
        ))
