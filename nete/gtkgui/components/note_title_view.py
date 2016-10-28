from gi.repository import Gdk, Gtk, GObject
from nete.gtkgui.actions import (
    change_note_title, finish_edit_mode_title,
    toggle_edit_mode_text, toggle_edit_mode_title)
from flurx import create_component


def create_note_title_view(store):
    return create_component(NoteTitleView, store, map_state_to_props)


def map_state_to_props(state):
    return (
        ('id', state['current_note']['id']),
        ('title', state['current_note']['note_title']),
        ('mode', 'edit' if state['ui_state']['is_editing_title'] else 'view'),
        ('text_edit_mode', 'edit' if state['ui_state']['is_editing_text'] else 'view'),
    )


class NoteTitleView(Gtk.Box):

    id = GObject.property(type=str)
    title = GObject.property(type=str)
    mode = GObject.property(type=str)
    text_edit_mode = GObject.property(type=str)

    def __init__(self):
        super().__init__(spacing=6)

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.bind_property('title', self.title_editor, 'title', GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property('title', self.title_view, 'title', GObject.BindingFlags.DEFAULT)

        self.connect('notify::title', self._on_notify_title)
        self.connect('notify::mode', self._on_notify_mode)
        self.connect('notify::text-edit-mode', self._on_notify_text_edit_mode)

        self.title_view.connect('double-clicked', lambda source: toggle_edit_mode_title())
        self.title_editor.connect('finished-edit', lambda source: finish_edit_mode_title())
        self.edit_button.connect('clicked', self._on_edit_button_click)

    def _on_title_view_double_clicked(self, *args):
        toggle_edit_mode_title()

    def _on_edit_button_click(self, *args):
        toggle_edit_mode()

    def _on_notify_title(self, *args):
        change_note_title(self.get_property('id'), self.get_property('title'))

    def _on_notify_mode(self, *args):
        self.title_stack.set_visible_child_name(self.get_property('mode'))

        if self.get_property('mode') == 'edit':
            self.title_editor.grab_focus()

    def _on_notify_text_edit_mode(self, *args):
        label_text = (
            'Edit' if self.get_property('text-edit-mode') == 'view'
            else 'Done')
        self.edit_button.set_label(label_text)

    def _build_ui(self):
        self.title_view = TitleView()
        self.title_editor = TitleEditor()

        self.title_stack = Gtk.Stack()
        self.title_stack.add_named(self.title_view, 'view')
        self.title_stack.add_named(self.title_editor, 'edit')
        self.title_stack.set_visible_child_name('view')

        self.edit_button = Gtk.Button.new_with_label('Edit')

        self.pack_start(self.title_stack, True, True, 0)
        self.pack_end(self.edit_button, False, False, 2)


class TitleView(Gtk.EventBox):

    title = GObject.property(type=str)

    __gsignals__ = {
        'double-clicked': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect('button-press-event', self._on_text_view_button_press)
        self.connect('notify::title', self._on_notify_title)

    def _on_text_view_button_press(self, source, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            self.emit('double-clicked')
        return False

    def _on_notify_title(self, *args):
        self.label.set_text(self.get_property('title'))

    def _build_ui(self):
        self.label = Gtk.Label(hexpand=True)
        self.add(self.label)


class TitleEditor(Gtk.Box):

    title = GObject.property(type=str)

    __gsignals__ = {
        'finished-edit': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_events()

    def grab_focus(self):
        self.entry.grab_focus()

    def _connect_events(self):
        self.bind_property('title', self.entry, 'text', GObject.BindingFlags.BIDIRECTIONAL)
        self.entry.connect('key-press-event', self._on_key_press_event)

    def _on_key_press_event(self, source, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_Return):
            self.emit('finished-edit')

    def _build_ui(self):
        self.entry = Gtk.Entry()

        self.pack_start(self.entry, True, True, 0)
