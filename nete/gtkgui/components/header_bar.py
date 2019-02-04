from gi.repository import Gtk
from fluous.gobject import connect


class HeaderBar(Gtk.HeaderBar):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_ui()

    def _build_ui(self):
        self.set_show_close_button(True)


def map_state_to_props(state):
    note_title = state['current_note']['title'] if state['current_note'] else 'No note loaded'
    return (
        ('title', '%s (nete%s)' % (
            note_title, '-DEVELOPMENT' if state['development_mode'] else '',
        )),
    )


def map_dispatch_to_props(dispatch):
    return {}


ConnectedHeaderBar = connect(HeaderBar, map_state_to_props, map_dispatch_to_props)
