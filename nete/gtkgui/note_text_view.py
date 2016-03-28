from gi.repository import Gdk, Gtk, GObject, WebKit
from nete.gtkgui.state.actions import change_note_text, finish_edit_note_title
from fluous.gobject import connect
import markdown


def map_state_to_props(state):
    return (
        ('note_id', state['current_note_id']),
        ('text', state['note_text']),
        ('mode', 'edit' if state['is_editing_text'] else 'view'),
    )


def map_dispatch_to_props(dispatch):
    return {
        'text-changed': lambda note_id, text:
            dispatch(change_note_text(note_id, text)),
    }


class NoteTextView(Gtk.Stack):

    note_id = GObject.property(type=str, default='')
    text = GObject.property(type=str, default='')
    mode = GObject.property(type=str, default='view')

    __gsignals__ = {
        'text-changed': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str, str)),
    }

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::text', lambda source, param: self._on_notify_text())
        self.connect('notify::mode', lambda source, param: self._on_notify_mode())
        self._text_editor_text_changed_handler = self.text_editor.get_buffer().connect(
            'notify::text',
            lambda source, event: self.emit(
                'text-changed',
                self.note_id,
                self.text_editor.get_buffer().get_property('text')))

    def _on_notify_text(self):
        if self.get_property('text') is None:
            return

        if self.get_property('mode') == 'view':
            html_text = markdown.markdown(self.get_property('text'))
            self.web_view.load_html_string(html_text, 'file://.')

    def _on_notify_mode(self):
        if self.get_property('mode') == 'view':
            html_text = markdown.markdown(self.get_property('text'))
            self.web_view.load_html_string(html_text, 'file://.')
            self.set_visible_child_name('view')
        elif self.get_property('mode') == 'edit':
            self.text_editor.get_buffer().set_property('text', self.get_property('text'))
            self.text_editor.grab_focus()
            self.set_visible_child_name('editor')

    def _build_ui(self):
        self.add_named(self._build_text_view(), 'view')
        self.add_named(self._build_text_editor(), 'editor')
        self.set_visible_child_name('view')

    def _build_text_view(self):
        scrollable_text_view = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.web_view = WebKit.WebView()
        scrollable_text_view.add(self.web_view)

        return scrollable_text_view

    def _build_text_editor(self):
        scrollable_text_editor = Gtk.ScrolledWindow( hexpand=True, vexpand=True)

        self.text_editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.text_editor.get_buffer()
        scrollable_text_editor.add(self.text_editor)

        return scrollable_text_editor


ConnectedNoteTextView = connect(NoteTextView, map_state_to_props, map_dispatch_to_props)
