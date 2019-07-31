from fluous.gobject import connect
from gi.repository import Gtk, GObject
from nete.gui.actions import (
    toggle_edit_note_text,
)


class Toolbar(Gtk.Box):

    text_edit_mode = GObject.Property(type=str, default='view')

    __gsignals__ = {
        'toggle-edit-text':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
    }

    def __init__(self, **kwargs):
        super().__init__(spacing=6, **kwargs)

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect(
            'notify::text-edit-mode',
            lambda source, param: self._on_notify_text_edit_mode())

        self.edit_button.connect('clicked', self._on_edit_button_click)

    def _on_edit_button_click(self, source):
        self.emit('toggle-edit-text')

    def _on_notify_text_edit_mode(self):
        if self.get_property('text-edit-mode') == 'view':
            self.edit_button.props.label = 'Edit'
        else:
            self.edit_button.props.label = 'Done'

    def _build_ui(self):
        self.edit_button = Gtk.Button(label='Edit', can_focus=False)
        self.pack_end(self.edit_button, False, False, 2)


def map_state_to_props(state):
    return (
        ('text_edit_mode', (
            'edit'
            if state['ui']['focus'] == 'note_editor'
            else 'view')),
    )


def map_dispatch_to_props(dispatch):
    return {
        'toggle-edit-text': lambda source:
            dispatch(toggle_edit_note_text()),
    }


ConnectedToolbar = connect(
    Toolbar,
    map_state_to_props,
    map_dispatch_to_props)
