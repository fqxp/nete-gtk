from fluous.gobject import connect
from gi.repository import Gdk, Gtk, GObject
from nete.gui.actions import (
    cancel_edit_note_title,
    finish_edit_note_title,
    toggle_edit_note_title,
)


class NoteTitle(Gtk.Box):

    title = GObject.Property(type=str)
    mode = GObject.Property(type=str, default='view')

    __gsignals__ = {
        'finish-edit-title':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str, )),
        'cancel-edit-title':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'toggle-edit-title':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
    }

    def __init__(self, **kwargs):
        super().__init__(can_focus=False, **kwargs)

        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.title_label = Gtk.Label(
            label=self.props.title,
            justify=Gtk.Justification.RIGHT,
        )

        self.title_editor = Gtk.Entry(
            name='note_title_editor',
            width_chars=40,
        )

        self.title_stack = Gtk.Stack(homogeneous=False)
        self.title_stack.add_named(self.title_label, 'view')
        self.title_stack.add_named(self.title_editor, 'editor')
        self.title_stack.set_visible_child_name(self.props.mode)
        self.pack_start(self.title_stack, True, True, 0)

        self.edit_title_button = Gtk.Button(
            name='edit-title-button',
            image=Gtk.Image(
                icon_name='document-edit-symbolic',
                icon_size=Gtk.IconSize.BUTTON,
                margin=0
            ),
            can_focus=False,
            relief=Gtk.ReliefStyle.NONE,
        )
        self.pack_start(self.edit_title_button, False, False, 4)

        self._update_title()

    def _connect_events(self):
        self.connect('notify::title', lambda source, params:
                     self._update_title())
        self.connect(
            'notify::mode',
            lambda source, param: self._on_notify_mode())
        self.bind_property(
            'title',
            self.title_editor,
            'text',
            GObject.BindingFlags.DEFAULT)

        self.edit_title_button.connect('clicked',
                                       lambda source: self.emit('toggle-edit-title'))

        self.title_editor.connect('activate',
                                  self._on_entry_activate)
        self.title_editor.connect('focus-out-event',
                                  self._on_entry_focus_out)
        self.title_editor.connect('key-press-event',
                                  self._on_key_press_event)

    def _update_title(self):
        title = self.props.title if self.props.title else 'No note loaded'
        self.title_label.props.label = title

    def _on_notify_mode(self):
        if self.props.mode == 'view':
            self.title_stack.set_visible_child_name('view')
        elif self.props.mode == 'edit':
            self.title_stack.set_visible_child_name('editor')

    def _on_entry_activate(self, source):
        self.emit('finish-edit-title', source.props.text)

    def _on_entry_focus_out(self, source, event):
        self.emit('finish-edit-title', source.props.text)

    def _on_key_press_event(self, source, event):
        if event.keyval == Gdk.KEY_Escape:
            self.emit('cancel-edit-title')


def map_state_to_props(state):
    title = (state['current_note']['title']
             if state['current_note']
             else None)

    return (
        ('title', title),
        ('mode', (
            'edit'
            if state['ui']['focus'] == 'note_title_editor'
            else 'view')),
    )


def map_dispatch_to_props(dispatch):
    return {
        'finish-edit-title': lambda source, new_title:
            dispatch(finish_edit_note_title(new_title)),
        'cancel-edit-title': lambda source, param:
            dispatch(cancel_edit_note_title()),
        'toggle-edit-title': lambda source:
            dispatch(toggle_edit_note_title()),
    }


ConnectedNoteTitle = connect(
    NoteTitle,
    map_state_to_props,
    map_dispatch_to_props)
