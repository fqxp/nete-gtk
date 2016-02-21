from gi.repository import Gdk, Gtk, GObject
from nete.gtkgui.state.actions import change_note_title, finish_edit_note_title


class NoteTitleView(Gtk.Stack):

    note_id = GObject.property(type=str, default='')
    title = GObject.property(type=str, default='')

    def __init__(self, store):
        super().__init__()

        self.connect_events()
        self.build_ui()

        store.subscribe(self.set_state)
        self.connect_store(store)
        self.set_state(store.state)

    def connect_events(self):
        self.connect('notify::title', lambda source, param: self.on_notify_title())

    def on_notify_title(self):
        if self.get_property('title') is None:
            return

        self.title_view.set_text(self.get_property('title'))

    def set_state(self, state):
        if state['current_note_id'] != self.get_property('note_id'):
            self.set_property('note_id', state['current_note_id'])

        if state['is_editing_title'] and self.edit_mode() == 'view':
            self.enable_edit_mode()

        if not state['is_editing_title'] and self.edit_mode() == 'editor':
            self.enable_view_mode()

        if state['note_title'] != self.get_property('title'):
            self.set_property('title', state['note_title'])

    def connect_store(self, store):
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

    def edit_mode(self):
        return self.get_visible_child_name()

    def enable_view_mode(self):
        self.set_visible_child_name('view')

    def enable_edit_mode(self):
        self.title_editor.set_text(self.get_property('title'))
        self.title_editor.grab_focus()
        self.set_visible_child_name('editor')

    def build_ui(self):
        self.title_view = Gtk.Label(hexpand=True)
        self.title_editor = Gtk.Entry()
        self.add_named(self.title_view, 'view')
        self.add_named(self.title_editor, 'editor')
        self.set_visible_child_name('view')
