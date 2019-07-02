from fluous.gobject import connect
from gi.repository import Gtk, GObject, WebKit2
import commonmark

from ..actions import change_cursor_position, change_note_text


class NoteTextView(Gtk.Stack):

    text = GObject.Property(type=str, default='')
    cursor_position = GObject.Property(type=int, default=0)
    mode = GObject.Property(type=str, default='view')

    __gsignals__ = {
        'text-changed': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'cursor-position-changed': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_ui()
        self._update_view()
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::mode', lambda source, param: self._update_view())
        self.connect('notify::text', lambda source, param: self._update_view())

        self.bind_property(
            'text',
            self.text_editor,
            'text',
            GObject.BindingFlags.DEFAULT)
        self.bind_property(
            'cursor-position',
            self.text_editor,
            'cursor-position',
            GObject.BindingFlags.DEFAULT)

        self.text_editor.connect(
            'text-changed',
            lambda source, text: (
                self.emit('text-changed', text)))
        self.text_editor.connect(
            'cursor-position-changed',
            lambda source, cursor_position: (
                self.emit('cursor-position-changed', cursor_position)))

    def _update_view(self):
        if self.get_property('mode') == 'view':
            self.text_view.set_property('text', self.get_property('text'))
            self.set_visible_child_name('view')
            self.text_view.grab_focus()
        elif self.get_property('mode') == 'edit':
            self.set_visible_child_name('editor')
            self.text_editor.grab_focus()

    def _build_ui(self):
        self.text_editor = TextEdit(text=self.get_property('text'))
        self.text_editor.show()
        self.add_named(self.text_editor, 'editor')

        self.text_view = TextView(text=self.get_property('text'))
        self.text_view.show()
        self.add_named(self.text_view, 'view')

        self.set_visible_child_name('view')


class TextView(Gtk.ScrolledWindow):

    text = GObject.Property(type=str, default='')

    def __init__(self, **kwargs):
        super().__init__(hexpand=True, vexpand=True, **kwargs)

        self.web_view = WebKit2.WebView()
        self.add(self.web_view)

        self.update_view()
        self.connect('notify::text', lambda source, params: self.update_view())

    def update_view(self):
        html_text = commonmark.commonmark(self.get_property('text'))
        self.web_view.load_html(html_text, 'file://.')
        self.web_view.grab_focus()

    def grab_focus(self):
        self.web_view.grab_focus()


class TextEdit(Gtk.Box):

    cursor_position = GObject.Property(type=int, default=0)
    text = GObject.Property(type=str, default='')

    __gsignals__ = {
        'cursor-position-changed': (GObject.SignalFlags.RUN_FIRST, None, (int, )),
        'text-changed': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
        self._connect_events()

    def grab_focus(self):
        self.text_editor.grab_focus()

    def _connect_events(self):
        self._text_buffer_changed_handler = self.text_buffer.connect(
            'changed',
            self._on_text_buffer_changed)
        self.connect('notify::text', self._on_notify_text)

        self._text_buffer_notify_cursor_position_handler = (
            self.text_buffer.connect(
                'notify::cursor-position',
                self._on_text_buffer_notify_cursor_position))
        self.connect(
            'notify::cursor-position',
            self._on_notify_cursor_position)

    def _on_text_buffer_changed(self, source):
        self.emit('text-changed', source.get_property('text'))

    def _on_notify_text(self, source, param):
        if self.text_buffer.get_property('text') == self.get_property('text'):
            return

        with self.text_buffer.handler_block(self._text_buffer_changed_handler):
            self.text_buffer.set_property('text', self.get_property('text'))

    def _on_text_buffer_notify_cursor_position(self, source, param):
        self.emit(
            'cursor-position-changed',
            self.text_buffer.get_property('cursor-position'))

    def _on_notify_cursor_position(self, source, param):
        if (self.text_buffer.get_property('cursor-position') ==
                self.get_property('cursor-position')):
            return

        with self.text_buffer.handler_block(
            self._text_buffer_notify_cursor_position_handler
        ):
            self.text_buffer.place_cursor(
                self.text_buffer.get_iter_at_offset(
                    self.get_property('cursor-position')))

    def _build_ui(self):
        self.pack_start(self._build_text_editor(), True, True, 0)

    def _build_text_editor(self):
        scrollable_text_editor = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.text_editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.text_editor.get_buffer()
        scrollable_text_editor.add(self.text_editor)
        self.text_buffer = self.text_editor.get_buffer()
        self.text_buffer.set_text(self.get_property('text'))

        return scrollable_text_editor


def map_state_to_props(state):
    return (
        ('text', (state['current_note']['text']
                  if state['current_note']
                  else None)),
        ('cursor-position', (
            state['current_note']['cursor_position']
            if state['current_note']
            else 0)),
        ('mode', 'edit' if state['ui']['focus'] == 'note_editor' else 'view'),
    )


def map_dispatch_to_props(dispatch):
    return {
        'text-changed': lambda source, text: dispatch(change_note_text(text)),
        'cursor-position-changed': lambda source, cursor_position:
            dispatch(change_cursor_position(cursor_position)),
    }


ConnectedNoteTextView = connect(
    NoteTextView,
    map_state_to_props,
    map_dispatch_to_props)
