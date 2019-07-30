from gi.repository import Gtk
from fluous.gobject import connect

from nete.gui.components.note_title import ConnectedNoteTitle
from nete.gui.components.note_collection_selector import ConnectedNoteCollectionSelector


class HeaderBar(Gtk.HeaderBar):

    def __init__(self, build_component, **kwargs):
        super().__init__(can_focus=False, **kwargs)

        self._build_ui(build_component)

    def _build_ui(self, build_component):
        self.set_show_close_button(True)

        self.note_collection_selector = build_component(ConnectedNoteCollectionSelector)
        self.pack_start(self.note_collection_selector)

        self.note_title = build_component(ConnectedNoteTitle)
        self.set_custom_title(self.note_title)


ConnectedHeaderBar = connect(HeaderBar)
