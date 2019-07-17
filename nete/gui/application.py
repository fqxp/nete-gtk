import logging
import sys

from gi.repository import Gtk, Gio, GLib
from fluous.store import Store
from fluous.reducer_decorators import debug_reducer

from nete.gui.actions import (
    load_configuration,
    load_notes,
    load_ui_state,
    save_note,
    save_ui_state,
)
from nete.gui.components.main_window import ConnectedMainWindow
from nete.gui.reducers import reducer
from nete.gui.state import selectors, initial_state
from nete.utils import in_development_mode, version


class Application(Gtk.Application):

    debug_mode = False

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id=self._application_id(),
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.set_property('register-session', True)
        self.window = None

        self.setup_options()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains('version'):
            print('nete {}'.format(version()))
            sys.exit(0)
        elif options.contains('debug'):
            self.debug_mode = True

        self.activate()

        return 0

    def do_activate(self):
        self.setup_logging(self.debug_mode)

        actual_reducer = reducer
        if self.debug_mode:
            actual_reducer = debug_reducer(
                print_state=False,
                print_diff=True,
                print_traceback=False)(reducer)
        self.store = Store(actual_reducer, initial_state)

        self.store.dispatch(load_configuration())
        self.store.dispatch(load_notes())
        self.store.dispatch(load_ui_state())

        self.window = ConnectedMainWindow(self.store)

        self.store.subscribe(
            lambda note, dispatch: dispatch(save_note(note)),
            selectors.current_note)
        self.store.subscribe(
            lambda ui_state, dispatch: dispatch(save_ui_state(ui_state)),
            selectors.ui_state)

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

    def _application_id(self):
        return 'de.fqxp.nete%s' % ('-dev' if in_development_mode() else '')
