from fluous.gobject import connect
from gi.repository import Gtk, GObject
from nete.gui.components.note_text_view import ConnectedNoteTextView
from nete.gui.components.note_title_view import ConnectedNoteTitleView


class NoteView(Gtk.Box):

    is_note_selected = GObject.Property(type=bool, default=False)
    widget = GObject.Property(type=GObject.TYPE_PYOBJECT, default=None)

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.build_component = build_component
        self._build_ui()
        self._update_visibility()
        self._connect_events()

    def _build_ui(self):
        self.box = Gtk.Box()
        self.pack_start(self.box, expand=True, fill=True, padding=0)

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
        if self.widget:
            self.widget.destroy()

        if self.get_property('is-note-selected'):
            self.widget = self._build_note_grid()
        else:
            self.widget = self._build_no_note_label()

        self.box.pack_start(self.widget, expand=True, fill=True, padding=0)
        self.show_all()


def map_state_to_props(state):
    return (
        ('is-note-selected', state['current_note'] is not None),
    )


ConnectedNoteView = connect(NoteView, map_state_to_props)
