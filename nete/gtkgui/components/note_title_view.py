from gi.repository import Gdk, Gtk, GObject
from nete.gtkgui.actions import change_note_title, finish_edit_note_title, toggle_edit_note_text
from fluous.gobject import connect


def map_state_to_props(state):
    return (
        ('note_id', state['ui_state']['current_note_id']),
        ('title', state['current_note']['note_title']),
        ('mode', 'edit' if state['ui_state']['is_editing_title'] else 'view'),
        ('text_edit_mode', 'edit' if state['ui_state']['is_editing_text'] else 'view'),
    )


def map_dispatch_to_props(dispatch):
    return {
        'title-changed': lambda note_id, text:
            dispatch(change_note_title(note_id, text)),
        'finish-edit': lambda note_id:
            dispatch(finish_edit_note_title()),
        'toggle-edit-text': lambda:
            dispatch(toggle_edit_note_text()),
    }


class NoteTitleView(Gtk.Box):

    note_id = GObject.property(type=str, default='')
    title = GObject.property(type=str, default='')
    mode = GObject.property(type=str, default='view')
    text_edit_mode = GObject.property(type=str, default='view')

    __gsignals__ = {
        'title-changed': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str, str)),
        'finish-edit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str,)),
        'toggle-edit-text': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, tuple()),
    }

    def __init__(self):
        super().__init__(spacing=6)

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::title', lambda source, param: self._on_notify_title())
        self.connect('notify::mode', lambda source, param: self._on_notify_mode())
        self.connect('notify::text-edit-mode', lambda source, param: self._on_notify_text_edit_mode())

        self._changed_title_handler = self.title_editor.connect(
            'notify::text',
            lambda source, param: self.emit('title-changed', self.note_id, self.title_editor.get_text()))

        self.title_editor.connect(
            'key-press-event',
            lambda source, event: self._on_key_press_event(event))

        self.edit_button.connect(
            'clicked',
            lambda source: self._on_edit_button_click())

    def _on_key_press_event(self, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_Return):
            self.emit('finish-edit', self.note_id)

    def _on_notify_title(self):
        if self.get_property('title') is None:
            return

        self.title_view.set_text(self.get_property('title'))

    def _on_edit_button_click(self):
        self.emit('toggle-edit-text')

    def _on_notify_mode(self):
        if self.get_property('mode') == 'view':
            self.title_stack.set_visible_child_name('view')
        elif self.get_property('mode') == 'edit':
            with self.title_editor.handler_block(self._changed_title_handler):
                self.title_editor.set_text(self.get_property('title'))
            self.title_editor.grab_focus()
            self.title_stack.set_visible_child_name('editor')

    def _on_notify_text_edit_mode(self):
        if self.get_property('text-edit-mode') == 'view':
            self.edit_button.set_label('Edit')
        else:
            self.edit_button.set_label('Done')

    def _build_ui(self):
        self.title_stack = Gtk.Stack()
        self.title_view = Gtk.Label(hexpand=True)
        self.title_editor = Gtk.Entry()
        self.title_stack.add_named(self.title_view, 'view')
        self.title_stack.add_named(self.title_editor, 'editor')
        self.title_stack.set_visible_child_name('view')

        self.edit_button = Gtk.Button.new_with_label('Edit')

        self.pack_start(self.title_stack, True, True, 0)
        self.pack_end(self.edit_button, False, False, 2)


ConnectedNoteTitleView = connect(NoteTitleView, map_state_to_props, map_dispatch_to_props)
