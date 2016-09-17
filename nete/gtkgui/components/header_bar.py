from nete.utils import in_development_mode
from gi.repository import Gtk, GObject
from fluous.gobject import connect


class HeaderBar(Gtk.HeaderBar):

    def __init__(self):
        Gtk.HeaderBar.__init__(self)

        self._build_ui()

    def _build_ui(self):
        self.set_show_close_button(True)


def map_state_to_props(state):
    return (
        ('title', '%s (nete%s)' % (
            state['current_note']['note_title'],
            '-DEVELOPMENT' if in_development_mode() else '',
        )),
    )


def map_dispatch_to_props(dispatch):
    return {
    }


ConnectedHeaderBar = connect(HeaderBar, map_state_to_props, map_dispatch_to_props)
