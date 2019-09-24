from fluous.gobject import connect
from gi.repository import Gtk, GLib, GObject
from nete.components.info_bar import ConnectedInfoBar
from nete.components.note_text_view import ConnectedNoteTextView
from nete.components.toolbar import ConnectedToolbar


class NoteView(Gtk.Bin):

    is_note_selected = GObject.Property(type=bool, default=False)
    widget = GObject.Property(type=GObject.TYPE_PYOBJECT, default=None)

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.build_component = build_component
        self._build_ui()
        self._update_visibility()
        self._connect_events()

    def _build_ui(self):
        box = Gtk.VBox()
        self.add(box)

        self.stack = Gtk.Stack()
        self.stack.add_named(self._build_no_note_label(), 'no-note-view')
        self.stack.add_named(self._build_note_grid(), 'note-view')

        box.pack_start(self.stack, True, True, 0)

        self.info_bar = self.build_component(ConnectedInfoBar)
        box.pack_start(self.info_bar, False, False, 0)

    def _build_no_note_label(self):
        return Gtk.Label(label='No note selected')

    def _build_note_grid(self):
        grid = Gtk.Grid()

        toolbar = self.build_component(ConnectedToolbar)
        grid.attach(toolbar, left=0, top=0, width=1, height=1)

        text_view = self.build_component(ConnectedNoteTextView)
        grid.attach(text_view, left=0, top=1, width=1, height=1)

        return grid

    def _connect_events(self):
        self.connect('notify::is-note-selected',
                     lambda source, param: self._update_visibility())

    def _update_visibility(self):
        if self.get_property('is-note-selected'):
            self.stack.set_visible_child_name('note-view')
        else:
            self.stack.set_visible_child_name('no-note-view')


def map_state_to_props(state):
    return (
        ('is-note-selected', state['current_note'] is not None),
    )


ConnectedNoteView = connect(NoteView, map_state_to_props)
