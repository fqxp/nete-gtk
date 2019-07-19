from fluous.gobject import connect
from gi.repository import Gtk, GtkSource, GObject, WebKit2
import commonmark

from nete.gui.actions import change_cursor_position, change_note_text
from nete.gui.resources import (
    template_resource,
    stylesheet_filename,
)


class NoteTextView(Gtk.Stack):

    text = GObject.Property(type=str, default='')
    cursor_position = GObject.Property(type=int, default=0)
    mode = GObject.Property(type=str, default='view')

    __gsignals__ = {
        'text-changed':
            (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'cursor-position-changed':
            (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    def __init__(self, **kwargs):
        super().__init__(can_focus=False, **kwargs)

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
        elif self.get_property('mode') == 'edit':
            self.set_visible_child_name('editor')

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
        super().__init__(
            hexpand=True,
            vexpand=True,
            can_focus=False,
            **kwargs)

        self.web_view = WebKit2.WebView(name='note_view')
        self.add(self.web_view)

        self.update_view()
        self.connect('notify::text', lambda source, params: self.update_view())

    def update_view(self):
        self.web_view.load_html(
            self.render_text(self.get_property('text')),
            'file://.')

    def render_text(self, text):
        stylesheet_url = stylesheet_filename('document')
        rendered_body = commonmark.commonmark(self.props.text)

        return template_resource('document').format(
            style_sheet_url=stylesheet_url,
            body=rendered_body)


class TextEdit(Gtk.Box):

    cursor_position = GObject.Property(type=int, default=0)
    text = GObject.Property(type=str, default='')

    __gsignals__ = {
        'cursor-position-changed':
            (GObject.SignalFlags.RUN_FIRST, None, (int, )),
        'text-changed':
            (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self._text_buffer_changed_handler = self.source_buffer.connect(
            'changed',
            self._on_text_buffer_changed)
        self.connect('notify::text', self._on_notify_text)

        self._text_buffer_notify_cursor_position_handler = (
            self.source_buffer.connect(
                'notify::cursor-position',
                self._on_text_buffer_notify_cursor_position))
        self.connect(
            'notify::cursor-position',
            self._on_notify_cursor_position)

    def _on_text_buffer_changed(self, source):
        self.emit('text-changed', source.get_property('text'))

    def _on_notify_text(self, source, param):
        if (self.source_buffer.get_property('text')
                == self.get_property('text')):
            return

        with self.source_buffer.handler_block(
                self._text_buffer_changed_handler):
            self.source_buffer.set_property('text', self.get_property('text'))

    def _on_text_buffer_notify_cursor_position(self, source, param):
        self.emit(
            'cursor-position-changed',
            self.source_buffer.get_property('cursor-position'))

    def _on_notify_cursor_position(self, source, param):
        if (self.source_buffer.get_property('cursor-position')
                == self.get_property('cursor-position')):
            return

        with self.source_buffer.handler_block(
                self._text_buffer_notify_cursor_position_handler):
            self.source_buffer.place_cursor(
                self.source_buffer.get_iter_at_offset(
                    self.get_property('cursor-position')))

    def _build_ui(self):
        self.pack_start(self._build_text_editor(), True, True, 0)

    def _build_text_editor(self):
        language_manager = GtkSource.LanguageManager.get_default()
        style_scheme_manager = GtkSource.StyleSchemeManager.get_default()

        scrollable_text_editor = Gtk.ScrolledWindow(hexpand=True, vexpand=True)

        self.source_buffer = GtkSource.Buffer()
        self.source_buffer.set_language(
            language_manager.get_language('markdown-nete'))
        self.source_buffer.set_style_scheme(
            style_scheme_manager.get_scheme('classic-nete'))

        self.text_editor = GtkSource.View(
            name='note_editor',
            buffer=self.source_buffer,
            monospace=True,
            insert_spaces_instead_of_tabs=True,
            tab_width=2,
            highlight_current_line=True,
            auto_indent=True,
            wrap_mode=Gtk.WrapMode.CHAR,
        )
        scrollable_text_editor.add(self.text_editor)
        self.source_buffer.set_text(self.props.text)

        return scrollable_text_editor


def map_state_to_props(state):
    return (
        ('text', (state['current_note']['text']
                  if state['current_note']
                  else '')),
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
