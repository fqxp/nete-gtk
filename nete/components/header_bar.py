from gi.repository import Gtk, GObject
from fluous.gobject import connect

from nete.components.note_title import ConnectedNoteTitle
from nete.components.note_collection_selector import ConnectedNoteCollectionSelector


class HeaderBar(Gtk.HeaderBar):

    development_mode = GObject.Property(type=bool, default=False)

    def __init__(self, build_component, **kwargs):
        super().__init__(can_focus=False, **kwargs)

        self._build_ui(build_component)

    def _build_ui(self, build_component):
        self.set_show_close_button(True)

        self.note_collection_selector = build_component(ConnectedNoteCollectionSelector)
        self.pack_start(self.note_collection_selector)

        if self.props.development_mode:
            development_mode_label = Gtk.Label(
                label='<b>DEVELOPMENT</b>',
                use_markup=True)
            self.pack_start(development_mode_label)

        self.note_title = build_component(ConnectedNoteTitle)
        self.set_custom_title(self.note_title)


def map_state_to_props(state):
    return (
        ('development_mode', state['development_mode']),
    )


ConnectedHeaderBar = connect(HeaderBar, map_state_to_props)
