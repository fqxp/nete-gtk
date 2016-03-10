from fluous.store import Store
from gi.repository import Gtk
from nete.services.storage_factory import create_storage
from nete.services.note_persistence import NotePersistence
from nete.gtkgui.main_window import MainWindow
from nete.gtkgui.state.action_types import *
from nete.gtkgui.state.actions import loaded_notes


initial_state = {
    'storage_uri': 'nete:notes',
    'current_note_id': None,
    'is_editing_title': False,
    'is_editing_text': False,
    'note_title': None,
    'note_text': None,
    'notes': [],
}


def logging_reducer(reducer):
    def logging_reducer(state, action):
        print('ACTION <%s>: %r' % (action['type'], action))

        new_state = reducer(state, action)

        print(dict(new_state.delete('notes')))

        return new_state
    return logging_reducer


def traceback_reducer(reducer):
    def traceback_reducer(state, action):
        import traceback ; traceback.print_stack()

        return reducer(state, action)
    return traceback_reducer


# @traceback_reducer
# @logging_reducer
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
    elif action_type == CHANGE_NOTE_TEXT:
        return state.set('note_text', action['text'])
    elif action_type == CHANGE_NOTE_TITLE:
        return state \
            .set('note_title', action['title']) \
            .set_by_path(('notes', action['note_id'], 'title'), action['title'])
    elif action_type == TOGGLE_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', not state['is_editing_text'])
    elif action_type == TOGGLE_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', not state['is_editing_title'])
    elif action_type == FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)
    elif action_type == FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)
    elif action_type == LOADED_NOTES:
        return state.set('notes', action['notes'])
    else:
        return state


class Application:

    def __init__(self):
        store = Store(reducer, initial_state)
        self.persistence = NotePersistence(store)

        self.load_notes(store, store.state['storage_uri'])

        self.main_window = MainWindow(store)
        self.main_window.connect("delete-event", Gtk.main_quit)

    def show_window(self):
        self.main_window.show_all()

    def load_notes(self, store, storage_uri):
        storage = create_storage(storage_uri)
        store.dispatch(loaded_notes(dict(
            (note_id, self._build_note_list_entry(storage.load(note_id)))
            for note_id in storage.list()
        )))

    def _build_note_list_entry(self, note):
        return {
            'title': note['title'],
        }
