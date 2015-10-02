from gi.repository import Gtk, GObject, WebKit
from .models.note import Note
import markdown


class NoteView(Gtk.Grid):

    def __init__(self, note=None):
        super().__init__()

        self.build_ui()

        self.note = note

        if note is not None:
            self.text_editor.get_buffer().connect('notify::text', self.on_text_buffer_text_changed)

        self.enable_view_mode()

    def on_text_buffer_text_changed(self, obj, note):
        self.note.text = self.text_editor.get_buffer().get_property('text')

    def toggle_edit_mode(self):
        if self.stack.get_visible_child_name() == 'editor':
            self.enable_view_mode()
        else:
            self.enable_edit_mode()

    def enable_view_mode(self):
        if self.note is not None:
            html_text = markdown.markdown(self.note.text)
        else:
            html_text = '<h3>No note selected</h3>'

        self.web_view.load_html_string(html_text, 'file://.')
        self.stack.set_visible_child_name('view')

    def enable_edit_mode(self):
        self.text_editor.get_buffer().set_text(self.note.text)
        self.stack.set_visible_child_name('editor')
        self.text_editor.grab_focus()

    def build_ui(self):
        self.stack = Gtk.Stack()
        self.attach(self.stack, 0, 0, 1, 1)

        text_view = self.build_text_view()
        self.stack.add_named(text_view, 'view')

        text_editor = self.build_text_editor()
        self.stack.add_named(text_editor, 'editor')

        self.stack.set_visible_child_name('view')

    def build_text_view(self):
        scrollable_text_view = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True)

        self.web_view = WebKit.WebView()
        scrollable_text_view.add(self.web_view)

        return scrollable_text_view

    def build_text_editor(self):
        scrollable_text_editor = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True)

        self.text_editor = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self.text_editor.get_buffer()
        scrollable_text_editor.add(self.text_editor)

        return scrollable_text_editor
