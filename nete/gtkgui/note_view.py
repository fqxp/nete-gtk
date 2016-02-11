from gi.repository import Gtk, GObject, WebKit, Gdk
from nete.gtkgui.state.actions import (
    change_note_text, change_note_title, finish_edit_note_title)
from .models.note import Note
import markdown


class NoteView(Gtk.Grid):

    def __init__(self, store):
        super().__init__()

        self.build_ui()

        self.note_id = None
        self.note_text = ''
        self.note_title = ''

        store.subscribe(self.on_state_changed)
        self.connect_store(store)
        self.on_state_changed(store.state)

    def on_state_changed(self, state):
        if state['current_note_id'] != self.note_id:
            self.note_id = state['current_note_id']

        if state['is_editing_text'] and self.edit_mode() == 'view':
            self.enable_text_edit_mode()
        elif not state['is_editing_text'] and self.edit_mode() == 'editor':
            self.enable_text_view_mode()

        if state['is_editing_title'] and self.title_edit_mode() == 'view':
            self.enable_title_edit_mode()
        elif not state['is_editing_title'] and self.title_edit_mode() == 'editor':
            self.enable_title_view_mode()

        if state['note_text'] != self.note_text:
            self.note_text = state['note_text']
            self.set_note_view_text(self.note_text)

        if state['note_title'] != self.note_title:
            self.note_title = state['note_title']

    def connect_store(self, store):
        self.text_editor.get_buffer().connect(
            'notify::text',
            lambda obj, data: store.dispatch(
                change_note_text(
                    self.note_id,
                    self.text_editor.get_buffer().get_property('text'))))

        self.title_editor.connect(
            'notify::text',
            lambda source, text: store.dispatch(
                change_note_title(
                    self.note_id,
                    self.title_editor.get_text())))

        self.title_editor.connect(
            'key-press-event',
            lambda source, event: store.dispatch(
                self.map_key_press_to_action(source, event)))

    def map_key_press_to_action(self, source, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_Return):
            return finish_edit_note_title()

    def set_note_view_text(self, text):
        html_text = markdown.markdown(text)
        self.web_view.load_html_string(html_text, 'file://.')

    def edit_mode(self):
        return self.stack.get_visible_child_name()

    def title_edit_mode(self):
        return self.title_stack.get_visible_child_name()

    def enable_text_view_mode(self):
        self.stack.set_visible_child_name('view')

    def enable_text_edit_mode(self):
        self.text_editor.get_buffer().set_text(self.note_text)
        self.title_editor.set_text(self.note_title)
        self.stack.set_visible_child_name('editor')
        self.text_editor.grab_focus()

    def enable_title_view_mode(self):
        self.title_view.set_text(self.note_title)
        self.title_stack.set_visible_child_name('view')

    def enable_title_edit_mode(self):
        self.title_stack.set_visible_child_name('editor')
        self.title_editor.grab_focus()

    def build_ui(self):
        self.title_stack = Gtk.Stack()
        self.attach(self.title_stack, 0, 0, 1, 1)

        self.title_view = self.build_title_view()
        self.title_editor = self.build_title_editor()
        self.title_stack.add_named(self.title_view, 'view')
        self.title_stack.add_named(self.title_editor, 'editor')
        self.title_stack.set_visible_child_name('view')

        self.stack = Gtk.Stack()
        self.attach(self.stack, 0, 1, 1, 1)

        text_view = self.build_text_view()
        text_editor = self.build_text_editor()
        self.stack.add_named(text_view, 'view')
        self.stack.add_named(text_editor, 'editor')
        self.stack.set_visible_child_name('view')

        self.show_all()

    def build_title_view(self):
        title_view = Gtk.Label(hexpand=True)

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
