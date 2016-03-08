from gi.repository import Gdk, Gtk, GObject
from nete.gtkgui.state.actions import change_note_title, finish_edit_note_title
from fluous.gobject import connect


def map_state_to_props(state):
    return {
        'note_id': state['current_note_id'],
        'title': state['note_title'],
        'mode': 'edit' if state['is_editing_title'] else 'view',
    }


def map_dispatch_to_props(dispatch):
    return {
        'title-changed': lambda note_id, text:
            dispatch(change_note_title(note_id, text)),
        'finish-edit': lambda note_id:
            dispatch(finish_edit_note_title()),
    }


class NoteTitleView(Gtk.Stack):

    note_id = GObject.property(type=str, default='')
    title = GObject.property(type=str, default='')
    mode = GObject.property(type=str, default='view')

    __gsignals__ = {
        'title-changed': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str, str)),
        'finish-edit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        self.build_ui()
        self.connect_events()

    def connect_events(self):
        self.connect('notify::title', lambda source, param: self.on_notify_title())
        self.connect('notify::mode', lambda source, param: self.on_notify_mode())

        self.title_editor.connect(
            'notify::text',
            lambda source, param: self.emit('title-changed', self.note_id, self.title_editor.get_text()))

        self.title_editor.connect(
            'key-press-event',
            lambda source, event: self._on_key_press_event(event))

    def _on_key_press_event(self, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_Return):
            self.emit('finish-edit', self.note_id)

    def on_notify_title(self):
        if self.get_property('title') is None:
            return

        self.title_view.set_text(self.get_property('title'))

    def on_notify_mode(self):
        if self.get_property('mode') == 'view':
            self.set_visible_child_name('view')
        elif self.get_property('mode') == 'edit':
            self.title_editor.set_text(self.get_property('title'))
            self.title_editor.grab_focus()
            self.set_visible_child_name('editor')

    def build_ui(self):
        self.title_view = Gtk.Label(hexpand=True)
        self.title_editor = Gtk.Entry()
        self.add_named(self.title_view, 'view')
        self.add_named(self.title_editor, 'editor')
        self.set_visible_child_name('view')


ConnectedNoteTitleView = connect(NoteTitleView, map_state_to_props, map_dispatch_to_props)
