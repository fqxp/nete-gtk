from nete.services.note_storage import save_note
from nete.services.ui_state_storage import save_ui_state
from nete.utils import in_development_mode
from .actions import (
    change_cursor_position, change_filter_term, change_note_text,
    change_note_title, create_note, finish_edit_note_text,
    finish_edit_note_title, load_note, load_notes, load_ui_state,
    loaded_note, loaded_notes, loaded_ui_state, move_paned,
    next_note, prev_note, quit, select_first, select_last,
    set_filter_term_entry_focus, toggle_edit_note_text,
    toggle_edit_note_title,
)
from .components.note_window import create_note_window
from .reducers import cache_reduce, current_note_reduce, ui_state_reduce
from .state import selectors
from flurx import combine_reducers, debug_reducer
from gi.repository import Gtk, Gio, GLib
from pyrsistent import freeze
from rx.subjects import BehaviorSubject, Subject
from rx.concurrency import GtkScheduler
import logging
import sys

logger = logging.getLogger(__name__)


initial_state = {
    'cache': {
        'notes': [],
    },
    'current_note': {
        'id': None,
        'note_title': '',
        'note_text': '',
        'cursor_position': 0,
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


scheduler = GtkScheduler()


actions = (
    change_filter_term,
    change_cursor_position,
    change_note_text,
    change_note_title,
    create_note,
    finish_edit_note_text,
    finish_edit_note_title,
    load_note,
    load_notes,
    load_ui_state,
    loaded_note,
    loaded_notes,
    loaded_ui_state,
    move_paned,
    next_note,
    prev_note,
    select_first,
    select_last,
    set_filter_term_entry_focus,
    toggle_edit_note_text,
    toggle_edit_note_title,
)


reducers = {
    'current_note': current_note_reduce,
    'ui_state': ui_state_reduce,
    'cache': cache_reduce,
}


class Application(Gtk.Application):

    debug_mode = False

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id=self._application_id(),
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.set_property('register-session', True)

        self.store = BehaviorSubject(freeze(initial_state))

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

        reducer = combine_reducers(reducers)

        if self.debug_mode:
            reducer = debug_reducer(print_traceback=False)(reducer)

        Subject().merge(*actions) \
            .map(self.resolve_action) \
            .filter(lambda action: action is not None) \
            .map(lambda action: reducer(self.store.value, action)) \
            .subscribe(self.store)

        load_notes()
        load_ui_state()

        note_ready_stream = BehaviorSubject(True)

        def do_save_note(note):
            note_ready_stream.on_next(False)
            future = save_note(note)
            future.add_done_callback(
                lambda f: note_ready_stream.on_next(True))

        note_stream = self.store \
            .map(selectors.current_note) \
            .distinct_until_changed() \
            .debounce(1000, scheduler=scheduler) \
            .pausable_buffered(note_ready_stream) \
            .subscribe(do_save_note)

        self.store \
            .map(selectors.ui_state) \
            .debounce(500, scheduler=scheduler) \
            .distinct_until_changed() \
            .subscribe(save_ui_state)

        quit.subscribe(self.do_quit)

        window = create_note_window(self.store)
        window.show_all()

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

    def resolve_action(self, action):
        while callable(action):
            action = action(state=self.store.value)

        return action

    def do_quit(self, data):
        Gtk.main_quit()

    def _application_id(self):
        return 'de.fqxp.nete%s' % ('-dev' if in_development_mode() else '')
