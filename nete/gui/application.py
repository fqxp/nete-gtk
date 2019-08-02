import logging
import sys

from gi.repository import Gtk, Gio, GLib
from fluous.store import Store
from fluous.gobject import register_store
from fluous.reducer_decorators import debug_reducer

from nete.gui.actions import (
    initialize,
    load_configuration,
    load_ui_state,
    reset,
    save_note,
    save_ui_state,
    select_note,
)
from nete.gui.components.main_window import ConnectedMainWindow
from nete.gui.reducer import reduce
from nete.gui.state import selectors, initial_state
from nete.utils import in_development_mode, version


class Application(Gtk.Application):

    debug_mode = False
    traceback = False

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id=self._application_id(),
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            register_session=True,
            **kwargs)
        GLib.set_application_name('nete')

        self.add_main_option_entries(self._command_line_options())
        self.window = None
        self.store = None

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains('version'):
            print('nete {}'.format(version()))
            sys.exit(0)

        self.debug_mode = options.contains('debug')
        self.traceback = options.contains('traceback')
        self.note_title = (
            command_line.get_arguments()[1]
            if len(command_line.get_arguments()) > 1
            else None)

        self.activate()
        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        self.setup_logging(self.debug_mode)

        if not self.window:
            actual_reduce = reduce
            if self.debug_mode:
                actual_reduce = debug_reducer(
                    print_state=False,
                    print_diff=True,
                    print_traceback=self.traceback)(actual_reduce)

            self.store = Store(actual_reduce, initial_state)

            self.store.dispatch(load_configuration())
            self.store.dispatch(initialize())
            self.store.dispatch(load_ui_state())
            self.store.dispatch(reset())
            self.store.subscribe(
                lambda note, dispatch: dispatch(save_note(note)),
                selectors.current_note)
            self.store.subscribe(
                lambda ui_state, dispatch: dispatch(save_ui_state(ui_state)),
                selectors.ui_state)

            register_store(self.store)

            self.window = ConnectedMainWindow()
            self.window.set_application(self)
            self.window.show_all()

        self.store.dispatch(select_note(self.note_title))

        self.window.present()

    def setup_logging(self, debug_mode):
        root_logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s [%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG if debug_mode else logging.WARN)

    def _command_line_options(self):
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

        option = GLib.OptionEntry()
        option.long_name = 'traceback'
        option.description = (
            'Enable traceback mode '
            '(when debug mode is also enabled)')
        options.append(option)

        return options

    def _application_id(self):
        return 'de.fqxp.nete%s' % ('-dev' if in_development_mode() else '')
