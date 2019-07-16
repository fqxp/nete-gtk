from fluous.gobject import connect
from gi.repository import Gdk, Gtk, GObject
from nete.gui.actions import (
    cancel_edit_note_title,
    finish_edit_note_title,
    toggle_edit_note_text,
    toggle_edit_note_title,
)


class NoteTitleView(Gtk.Box):

    mode = GObject.Property(type=str, default='view')
    text_edit_mode = GObject.Property(type=str, default='view')
    title = GObject.Property(type=str, default='')

    __gsignals__ = {
        'finish-edit':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str, )),
        'cancel-edit':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'toggle-edit-text':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'toggle-edit-title':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
    }

    def __init__(self, **kwargs):
        super().__init__(spacing=6, **kwargs)

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect(
            'notify::mode',
            lambda source, param: self._on_notify_mode())
        self.connect(
            'notify::text-edit-mode',
            lambda source, param: self._on_notify_text_edit_mode())

        self.bind_property(
            'title',
            self.title_editor,
            'text',
            GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property(
            'title',
            self.title_view,
            'label',
            GObject.BindingFlags.BIDIRECTIONAL)

        self.title_view_event_box.connect(
            'button-press-event',
            self._on_title_view_button_press)

        self.title_editor.connect('activate', self._on_entry_activate)
        self.title_editor.connect('focus-out-event', self._on_entry_focus_out)
        self.title_editor.connect('key-press-event', self._on_key_press_event)
        self.edit_button.connect('clicked', self._on_edit_button_click)

    def _on_entry_activate(self, source):
        self.emit('finish-edit', source.get_property('text'))

    def _on_entry_focus_out(self, source, event):
        self.emit('finish-edit', source.get_property('text'))

    def _on_key_press_event(self, source, event):
        if event.keyval == Gdk.KEY_Escape:
            self.emit('cancel-edit')

    def _on_title_view_button_press(self, source, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            self.emit('toggle-edit-title')
        return False

    def _on_edit_button_click(self, source):
        self.emit('toggle-edit-text')

    def _on_notify_mode(self):
        if self.get_property('mode') == 'view':
            self.title_stack.set_visible_child_name('view')
        elif self.get_property('mode') == 'edit':
            self.title_editor.grab_focus()
            self.title_stack.set_visible_child_name('editor')

    def _on_notify_text_edit_mode(self):
        if self.get_property('text-edit-mode') == 'view':
            self.edit_button.set_label('Edit')
        else:
            self.edit_button.set_label('Done')

    def _build_ui(self):
        self.title_view = Gtk.Label(label=self.title, hexpand=True)

        self.title_view_event_box = Gtk.EventBox()
        self.title_view_event_box.add(self.title_view)

        self.title_editor = Gtk.Entry(text=self.title)

        self.title_stack = Gtk.Stack()
        self.title_stack.add_named(self.title_view_event_box, 'view')
        self.title_stack.add_named(self.title_editor, 'editor')
        self.title_stack.set_visible_child_name('view')

        self.edit_button = Gtk.Button.new_with_label('Edit')

        self.pack_start(self.title_stack, True, True, 0)
        self.pack_end(self.edit_button, False, False, 2)


def map_state_to_props(state):
    return (
        ('title', (
            state['current_note']['title']
            if state['current_note']
            else '')),
        ('mode', (
            'edit'
            if state['ui']['focus'] == 'note_title_editor'
            else 'view')),
        ('text_edit_mode', (
            'edit'
            if state['ui']['focus'] == 'note_editor'
            else 'view')),
    )


def map_dispatch_to_props(dispatch):
    return {
        'finish-edit': lambda source, new_title:
            dispatch(finish_edit_note_title(new_title)),
        'cancel-edit': lambda source, param:
            dispatch(cancel_edit_note_title()),
        'toggle-edit-title': lambda source:
            dispatch(toggle_edit_note_title()),
        'toggle-edit-text': lambda source:
            dispatch(toggle_edit_note_text()),
    }


ConnectedNoteTitleView = connect(
    NoteTitleView,
    map_state_to_props,
    map_dispatch_to_props)
