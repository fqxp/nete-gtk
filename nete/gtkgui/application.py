from fluous.store import Store
from fluous.reducer_decorators import log_action, log_traceback, log_state_diff, log_state
from fluous.functions import combine_reducers
from .persistence.note_persistence import on_note_changed
from .persistence.ui_state_persistence import ConnectedUiStatePersistence
from .components.main_window import ConnectedMainWindow
from .state.actions import load_notes, load_ui_state
from .state import selectors
from . import reducers


initial_state = {
    'cache': {
        'notes': [],
    },
    'current_note': {
        'id': None,
        'note_title': None,
        'note_text': None,
        'needs_save': False,
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


reducer = combine_reducers({
    'current_note': reducers.current_note.reduce,
    'ui_state': reducers.ui_state.reduce,
    'cache': reducers.cache.reduce,
})
# reducer = log_state(reducer)


class Application:

    def __init__(self):
        store = Store(reducer, initial_state)

        store.dispatch(load_notes())
        store.dispatch(load_ui_state())

        store.subscribe(on_note_changed, selectors.current_note)

        self.ui_persistence = ConnectedUiStatePersistence(store)

        self.main_window = ConnectedMainWindow(store)

    def show_window(self):
        self.main_window.show_all()
