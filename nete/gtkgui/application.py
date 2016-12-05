from nete.gtkgui import streams
from nete.utils import in_development_mode
from .actions import load_notes, load_ui_state
from .components.note_window import create_note_window
from .store import store
from gi.repository import Gtk, Gio, GLib
import logging
import sys

logger = logging.getLogger(__name__)


class Application(Gtk.Application):

    debug_mode = False

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id=self._application_id(),
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.set_property('register-session', True)

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

        streams.setup_streams(store, self.debug_mode)

        load_notes()
        load_ui_state()

        window = create_note_window(store)
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

    def _application_id(self):
        return 'de.fqxp.nete%s' % ('-dev' if in_development_mode() else '')
