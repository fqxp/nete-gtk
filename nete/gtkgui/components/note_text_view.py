from gi.repository import Gdk, Gtk, GObject, WebKit
from nete.gtkgui.actions import change_note_text, change_cursor_position, finish_edit_note_title
from fluous.gobject import connect
import CommonMark


class NoteTextView(Gtk.Stack):

    note_id = GObject.property(type=str, default='')
    text = GObject.property(type=str, default='')
    cursor_position = GObject.property(type=int, default=3)
    mode = GObject.property(type=str, default='view')

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::mode', lambda source, param: self._on_notify_mode())

        self.bind_property('text', self.text_editor, 'text', GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property('cursor-position', self.text_editor, 'cursor-position', GObject.BindingFlags.BIDIRECTIONAL)
        self.connect('notify::text', self._on_notify_text)

    def _on_notify_text(self, source, param):
        if self.get_property('text') is None:
            return

        if self.get_property('mode') == 'view':
            html_text = CommonMark.commonmark(self.get_property('text'))
            self.web_view.load_html_string(html_text, 'file://.')

    def _on_notify_mode(self):
        if self.get_property('mode') == 'view':
            html_text = CommonMark.commonmark(self.get_property('text'))
            self.web_view.load_html_string(html_text, 'file://.')
            self.set_visible_child_name('view')

        elif self.get_property('mode') == 'edit':
            self.text_editor.grab_focus()
            self.set_visible_child_name('editor')

    def _build_ui(self):
        self.add_named(self._build_text_view(), 'view')
        self.add_named(self._build_text_editor(), 'editor')
        self.set_visible_child_name('view')

    def _build_text_editor(self):
        self.text_editor = TextEdit()
        return self.text_editor

    def _build_text_view(self):
        scrollable_text_view = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.web_view = WebKit.WebView()
        scrollable_text_view.add(self.web_view)

        return scrollable_text_view


class TextEdit(Gtk.Box):

    cursor_position = GObject.property(type=int, default=0)
    text = GObject.property(type=str, default='')

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._connect_events()

    def grab_focus(self):
        self.text_editor.grab_focus()

    def _connect_events(self):
        self.bind_property('text', self.text_buffer, 'text', GObject.BindingFlags.BIDIRECTIONAL)

        self._text_buffer_cursor_position_changed_handler = self.text_buffer.connect(
            'notify::cursor-position',
            lambda source, param:
                self.set_property('cursor-position', self.text_buffer.get_property('cursor-position')))
        self.connect('notify::cursor-position', self._on_notify_cursor_position)

    def _on_notify_cursor_position(self, source, param):
        if self.text_buffer.get_property('cursor-position') == self.get_property('cursor-position'):
            return

        with self.text_buffer.handler_block(self._text_buffer_cursor_position_changed_handler):
            self.text_buffer.place_cursor(
                self.text_buffer.get_iter_at_offset(
                    self.get_property('cursor-position')))

    def _build_ui(self):
        self.pack_start(self._build_text_editor(), True, True, 0)

    def _build_text_editor(self):
        scrollable_text_editor = Gtk.ScrolledWindow( hexpand=True, vexpand=True)

        self.text_editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.text_editor.get_buffer()
        scrollable_text_editor.add(self.text_editor)
        self.text_buffer = self.text_editor.get_buffer()

        return scrollable_text_editor


def map_state_to_props(state):
    return (
        ('note_id', state['ui_state']['current_note_id']),
        ('text', state['current_note']['note_text']),
        ('cursor-position', state['current_note']['cursor_position']),
        ('mode', 'edit' if state['ui_state']['is_editing_text'] else 'view'),
    )


def map_dispatch_to_props(dispatch):
    return {
        'notify::text': lambda source, param:
            dispatch(
                change_note_text(source.get_property('note_id'), source.get_property('text'))),
        'notify::cursor-position': lambda source, param:
            dispatch(change_cursor_position(source.get_property('cursor-position'))),
    }


ConnectedNoteTextView = connect(NoteTextView, map_state_to_props, map_dispatch_to_props)
