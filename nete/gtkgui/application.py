from fluous.store import Store
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff
from fluous.functions import combine_reducers
from .persistence.note_persistence import ConnectedNotePersistence
from .persistence.ui_state_persistence import ConnectedUiStatePersistence
from .components.main_window import ConnectedMainWindow
from .state.actions import load_notes, load_ui_state
from . import reducers


initial_state = {
    'cache': {
        'notes': [],
    },
    'current_note': {
        'id': None,
        'note_title': None,
        'note_text': None,
    },
    'ui_state': {
        'storage_uri': 'nete:notes',
        'is_editing_title': False,
        'is_editing_text': False,
        'current_note_id': None,
        'window_position': None,
        'window_size': [600, 400],
        'paned_position': 250,
   },
}


# @log_traceback
#@log_state_diff
#@log_action
#def reducer(state, action):
#    action_type = action['type']
#
#    else:
#        return state

reducer = combine_reducers({
    'current_note': reducers.current_note.reduce,
    'ui_state': reducers.ui_state.reduce,
    'cache': reducers.cache.reduce,
})


class Application:

    def __init__(self):
        store = Store(reducer, initial_state)

        store.dispatch(load_notes())
        store.dispatch(load_ui_state())

        self.persistence = ConnectedNotePersistence(store)
        self.ui_persistence = ConnectedUiStatePersistence(store)

        self.main_window = ConnectedMainWindow(store)

    def show_window(self):
        self.main_window.show_all()
