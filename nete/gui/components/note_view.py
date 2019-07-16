from fluous.gobject import connect
from gi.repository import Gtk, GObject
from nete.gui.components.note_text_view import ConnectedNoteTextView
from nete.gui.components.note_title_view import ConnectedNoteTitleView


class NoteView(Gtk.Stack):

    is_note_selected = GObject.Property(type=bool, default=False)
    widget = GObject.Property(type=GObject.TYPE_PYOBJECT, default=None)

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.build_component = build_component
        self._build_ui()
        self._update_visibility()
        self._connect_events()

    def _build_ui(self):
        self.add_named(self._build_no_note_label(), 'no-note-view')
        self.add_named(self._build_note_grid(), 'note-view')

        self.show_all()

    def _build_no_note_label(self):
        return Gtk.Label('No note selected')

    def _build_note_grid(self):
        grid = Gtk.Grid()

        title_view = self.build_component(ConnectedNoteTitleView)
        grid.attach(title_view, left=0, top=0, width=1, height=1)

        text_view = self.build_component(ConnectedNoteTextView)
        grid.attach(text_view, left=0, top=1, width=1, height=1)

        return grid

    def _connect_events(self):
        self.connect('notify::is-note-selected',
                     lambda source, param: self._update_visibility())

    def _update_visibility(self):
        if self.get_property('is-note-selected'):
            self.set_visible_child_name('note-view')
        else:
            self.set_visible_child_name('no-note-view')


def map_state_to_props(state):
    return (
        ('is-note-selected', state['current_note'] is not None),
    )


ConnectedNoteView = connect(NoteView, map_state_to_props)
