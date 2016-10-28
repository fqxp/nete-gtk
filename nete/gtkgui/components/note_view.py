from nete.gtkgui.actions import change_note_text, change_cursor_position
from .note_title_view import create_note_title_view
from gi.repository import Gtk, GObject, WebKit
from flurx import create_component
import CommonMark


def create_note_view(store):
    return create_component(NoteView, store, map_state_to_props)


def map_state_to_props(state):
    return (
        ('text', state['current_note']['note_text']),
        ('mode', 'edit' if state['ui_state']['is_editing_text'] else 'view'),
        ('cursor-position', state['current_note']['cursor_position']),
    )


class NoteView(Gtk.Stack):

    mode = GObject.property(type=str, default='view')
    text = GObject.property(type=str)
    cursor_position = GObject.property(type=int, default=0)

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

        self._text_before = None
        self._cursor_position_before = None

    def _connect_events(self):
        self.connect('notify::mode', self._on_notify_mode)
        self.connect('notify::text', self._on_notify_text)
        self.connect_after('notify::cursor-position', self._on_notify_cursor_position)

        self.bind_property(
            'text', self.note_editor, 'text',
            GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property(
            'text', self.rendered_note_view, 'text',
            GObject.BindingFlags.DEFAULT)
        self.bind_property(
            'cursor-position', self.note_editor, 'cursor-position',
            GObject.BindingFlags.BIDIRECTIONAL)

    def _on_notify_mode(self, *args):
        self.set_visible_child_name(self.get_property('mode'))

        if self.get_property('mode') == 'edit':
            self.note_editor.grab_focus()

    def _on_notify_text(self, *args):
        text = self.get_property('text')
        if text is None or self._text_before == text:
            return
        self._text_before = text

        change_note_text(text)

    def _on_notify_cursor_position(self, *args):
        cursor_position = self.get_property('cursor-position')
        if self._cursor_position_before == cursor_position:
            return
        self._cursor_position_before = cursor_position

        change_cursor_position(cursor_position)

    def _build_ui(self):
        self.rendered_note_view = RenderedNoteView()
        self.add_named(self.rendered_note_view, 'view')

        self.note_editor = NoteEditor()
        self.add_named(self.note_editor, 'edit')

        self.set_visible_child_name('view')


class RenderedNoteView(Gtk.Box):

    text = GObject.property(type=str)

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::text', self._on_notify_text)

    def _on_notify_text(self, *args):
        html_text = CommonMark.commonmark(self.get_property('text'))
        self.web_view.load_html_string(html_text, 'file://.')

    def _build_ui(self):
        scrollable_text_view = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.web_view = WebKit.WebView()
        scrollable_text_view.add(self.web_view)

        self.pack_start(scrollable_text_view, True, True, 0)


class NoteEditor(Gtk.Box):

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
        self.text_buffer.bind_property('cursor-position', self, 'cursor-position', GObject.BindingFlags.DEFAULT)
        self.connect('notify::cursor-position', self._on_notify_cursor_position)

    def _on_notify_cursor_position(self, source, param):
        if self.text_buffer.get_property('cursor-position') == self.get_property('cursor-position'):
            return

        iter = self.text_buffer.get_iter_at_offset(self.get_property('cursor-position'))
        self.text_buffer.place_cursor(iter)

    def _build_ui(self):
        scrollable_text_editor = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.text_editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.text_editor.get_buffer()
        scrollable_text_editor.add(self.text_editor)
        self.text_buffer = self.text_editor.get_buffer()

        self.pack_start(scrollable_text_editor, True, True, 0)
