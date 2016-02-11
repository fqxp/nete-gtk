from fluous.store import Store
from gi.repository import Gtk
from nete.gtkgui.models.note_list import NoteList
from nete.gtkgui.main_window import MainWindow
from nete.gtkgui.state.action_types import *


initial_state = {
    'current_note_id': None,
    'is_editing_title': False,
    'is_editing_text': False,
    'note_title': 'hjallo',
    'note_text': 'adasfdsa\nafasd',
}


def reducer(state, action):
    print('ACTION', action)

    action_type = action['type']

    if action_type == SELECT_NOTE:
        return state.set('current_note_id', action['note_id'])
    elif action_type == CHANGE_NOTE_TEXT:
        return state.set('note_text', action['text'])
    elif action_type == CHANGE_NOTE_TITLE:
        return state.set('note_title', action['title'])
    elif action_type == TOGGLE_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', not state['is_editing_text'])
    elif action_type == TOGGLE_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', not state['is_editing_title'])
    elif action_type == FINISH_EDIT_NOTE_TITLE:
        return state.set('is_editing_title', False)
    elif action_type == FINISH_EDIT_NOTE_TEXT:
        return state.set('is_editing_text', False)
    else:
        return state


class Application:

    def __init__(self):
        note_list = NoteList('nete:notes')
        note_list.load()

        store = Store(reducer, initial_state)

        self.main_window = MainWindow(store, note_list)
        self.main_window.connect("delete-event", Gtk.main_quit)

    def show_window(self):
        self.main_window.show_all()
