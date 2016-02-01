from gi.repository import Gtk, GObject, WebKit, Gdk
from .models.note import Note
import markdown


class NoteView(Gtk.Grid):

    def __init__(self, note=None):
        super().__init__()

        self.note = note

        if note is not None:
            self.build_ui()
            self.connect_signals()
            self.enable_title_view_mode()
            self.enable_text_view_mode()

    def toggle_edit_mode(self):
        if self.stack.get_visible_child_name() == 'editor':
            self.enable_text_view_mode()
        else:
            self.enable_text_edit_mode()

    def toggle_title_mode(self):
        if self.title_stack.get_visible_child_name() == 'editor':
            self.enable_title_view_mode()
        else:
            self.enable_title_edit_mode()

    def enable_text_view_mode(self):
        html_text = markdown.markdown(self.note.text)
        self.web_view.load_html_string(html_text, 'file://.')
        self.stack.set_visible_child_name('view')

    def enable_text_edit_mode(self):
        self.text_editor.get_buffer().set_text(self.note.text)
        self.stack.set_visible_child_name('editor')
        self.text_editor.grab_focus()

    def enable_title_view_mode(self):
        self.title_view.set_text(self.note.title)
        self.title_stack.set_visible_child_name('view')

    def enable_title_edit_mode(self):
        self.title_editor.set_text(self.note.title)
        self.title_stack.set_visible_child_name('editor')
        self.title_editor.grab_focus()

    def connect_signals(self):
        self.title_editor.connect('key-press-event', self.on_title_key_press)
        self.text_editor.get_buffer().connect('notify::text', self.on_text_buffer_text_changed)

    def on_text_buffer_text_changed(self, obj, note):
        self.note.text = self.text_editor.get_buffer().get_property('text')

    def on_title_key_press(self, source, event):
        if event.keyval == Gdk.KEY_Escape:
            self.enable_title_view_mode()
        elif event.keyval == Gdk.KEY_Return:
            self.note.title = self.title_editor.get_text()
            self.enable_title_view_mode()

    def build_ui(self):
        self.title_stack = Gtk.Stack()
        self.attach(self.title_stack, 0, 0, 1, 1)

        self.title_view = self.build_title_view()
        self.title_editor = self.build_title_editor()
        self.title_stack.add_named(self.title_view, 'view')
        self.title_stack.add_named(self.title_editor, 'editor')

        self.stack = Gtk.Stack()
        self.attach(self.stack, 0, 1, 1, 1)

        text_view = self.build_text_view()
        text_editor = self.build_text_editor()
        self.stack.add_named(text_view, 'view')
        self.stack.add_named(text_editor, 'editor')

    def build_title_view(self):
        title_view = Gtk.Label(label=self.note.title, hexpand=True)

        return title_view

    def build_title_editor(self):
        title_editor = Gtk.Entry()

        return title_editor

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
