from gi.repository import Gdk, Gtk, GObject, WebKit
from nete.gtkgui.state.actions import change_note_text
import markdown


class NoteTextView(Gtk.Stack):

    note_id = GObject.property(type=str, default='')
    text = GObject.property(type=str, default='')

    def __init__(self, store):
        super().__init__()

        self.build_ui()
        self.connect_events()

        store.subscribe(self.set_state)
        self.connect_store(store)
        self.set_state(store.state)

    def connect_events(self):
        self.connect('notify::text', lambda source, param: self.on_notify_text())

    def on_notify_text(self):
        if self.get_property('text') is None:
            return

        html_text = markdown.markdown(self.get_property('text'))
        self.web_view.load_html_string(html_text, 'file://.')

        if self.get_property('text') != self.text_editor.get_buffer().get_property('text'):
            self.text_editor.get_buffer().set_text(self.get_property('text'))

    def set_state(self, state):
        if state['current_note_id'] != self.get_property('note_id'):
            self.set_property('note_id', state['current_note_id'])

        if state['is_editing_text'] and self.edit_mode() == 'view':
            self.enable_edit_mode()

        if not state['is_editing_text'] and self.edit_mode() == 'editor':
            self.enable_view_mode()

        if state['note_text'] != self.get_property('text'):
            self.set_property('text', state['note_text'])

    def connect_store(self, store):
        self.text_editor.get_buffer().connect(
            'notify::text',
            lambda source, data: store.dispatch(
                change_note_text(
                    self.note_id,
                    self.text_editor.get_buffer().get_property('text'))))

    def edit_mode(self):
        return self.get_visible_child_name()

    def enable_view_mode(self):
        self.set_visible_child_name('view')

    def enable_edit_mode(self):
        self.text_editor.grab_focus()
        self.set_visible_child_name('editor')

    def build_ui(self):
        text_view = self.build_text_view()
        text_editor = self.build_text_editor()
        self.add_named(text_view, 'view')
        self.add_named(text_editor, 'editor')
        self.set_visible_child_name('view')

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
