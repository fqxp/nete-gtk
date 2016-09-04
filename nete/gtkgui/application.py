from gi.repository import Gtk, Gio, GLib
from fluous.store import Store
from fluous.reducer_decorators import debug_reducer
from fluous.functions import combine_reducers
from .persistence.note_persistence import on_note_changed
from .persistence.ui_state_persistence import on_ui_state_changed
from .components.main_window import ConnectedMainWindow
from .actions import load_notes, load_ui_state
from .state import selectors
from . import reducers
import logging
import sys


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


class Application(Gtk.Application):

    debug_mode = False

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, application_id="org.fqxp.nete",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.set_property('register-session', True)
        self.window = None

        self.setup_options()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains('version'):
            print('nete 0.0001 alpha')
            sys.exit(0)
        elif options.contains('debug'):
            self.debug_mode = True

        self.activate()

        return 0

    def do_activate(self):
        self.setup_logging(self.debug_mode)

        if self.debug_mode:
            global reducer
            reducer = debug_reducer()(reducer)
        self.store = Store(reducer, initial_state)

        self.window = ConnectedMainWindow(self.store)

        self.store.dispatch(load_notes())
        self.store.dispatch(load_ui_state())

        self.store.subscribe(on_note_changed, selectors.current_note)
        self.store.subscribe(on_ui_state_changed, selectors.ui_state)

        self.window.show_all()

    def setup_logging(self, debug_mode):
        root_logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s [%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG if debug_mode else logging.WARN)

    def setup_options(self):
        options = []

        option = GLib.OptionEntry()
        option.long_name = 'version'
        option.short_name = ord('v')
        option.description = 'Show program’s version number and exit'
        options.append(option)

        option = GLib.OptionEntry()
        option.long_name = 'debug'
        option.short_name = ord('D')
        option.description = 'Enable debug mode'
        options.append(option)

        self.add_main_option_entries(options)
