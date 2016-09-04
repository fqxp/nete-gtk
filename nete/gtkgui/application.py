from gi.repository import Gtk, Gio
from fluous.store import Store
from fluous.reducer_decorators import debug_reducer
from fluous.functions import combine_reducers
from .persistence.note_persistence import on_note_changed
from .persistence.ui_state_persistence import on_ui_state_changed
from .components.main_window import ConnectedMainWindow
from .actions import load_notes, load_ui_state
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
        'paned_position': 250,
        'filter_term_entry_focus': False,
        'filter_term': '',
   },
}


reducer = combine_reducers({
    'current_note': reducers.current_note.reduce,
    'ui_state': reducers.ui_state.reduce,
    'cache': reducers.cache.reduce,
})
reducer = debug_reducer()(reducer)


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, application_id="org.fqxp.nete",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.set_property('register-session', True)
        self.store = Store(reducer, initial_state)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.window = ConnectedMainWindow(self.store)

        self.store.dispatch(load_notes())
        self.store.dispatch(load_ui_state())

        self.store.subscribe(on_note_changed, selectors.current_note)
        self.store.subscribe(on_ui_state_changed, selectors.ui_state)

    def do_command_line(self, command_line):
        self.activate()
        return 0

    def do_activate(self):
        self.window.show_all()
