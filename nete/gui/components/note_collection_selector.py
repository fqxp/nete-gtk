from gi.repository import Gtk, GObject
from fluous.gobject import connect

from nete.gui.actions import select_collection


class NoteCollectionSelector(Gtk.ComboBoxText):

    current_note_collection_id = GObject.Property(type=str)
    note_collections = GObject.Property(type=GObject.TYPE_PYOBJECT)
    note_collection_chooser_has_focus = GObject.Property(type=bool, default=False)

    __gsignals__ = {
        'collection-selected':
            (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, build_component, **kwargs):
        super().__init__(
            name='note_collection_selector',
            can_focus=False,
            **kwargs
        )

        self._connect_events()
        self._update_note_collections()

    def _connect_events(self):
        self.bind_property(
            'current_note_collection_id',
            self,
            'active-id',
            GObject.BindingFlags.DEFAULT)

        self.connect(
            'changed',
            lambda source: self.emit('collection-selected', self.get_active_id()))
        self.connect(
            'notify::note-collections',
            self._on_notify_note_collections)
        self.connect(
            'notify::popup-shown',
            self._on_notify_collection_chooser_popup_shown)
        self.connect(
            'notify::note-collection-chooser-has-focus',
            self._on_notify_note_collection_chooser_has_focus)

    def _on_notify_note_collections(self, source, params):
        self._update_note_collections()

    def _update_note_collections(self):
        self.remove_all()

        for i, note_collection in enumerate(self.props.note_collections):
            self.append(
                note_collection.id,
                note_collection.name
            )
            if self.current_note_collection_id == note_collection.id:
                self.set_property('active', i)

    def _on_notify_note_collection_chooser_has_focus(self, source, params):
        if self.get_property('note-collection-chooser-has-focus'):
            self.popup()

    def _on_notify_collection_chooser_popup_shown(self, source, params):
        if not self.props.popup_shown:
            self.emit('collection-selected', self.get_active_id())


def map_state_to_props(state):
    return (
        ('note_collections',
         sorted(
             state['configuration'].note_collections,
             key=lambda collection: collection.name
         )),
        ('current_note_collection_id',
            state['ui']['current_note_collection_id']),
        ('note_collection_chooser_has_focus',
            state['ui']['focus'] == 'note_collection_selector'),
    )


def map_dispatch_to_props(dispatch):
    return {
        'collection-selected': lambda source, collection_id:
            dispatch(select_collection(collection_id)),
    }


ConnectedNoteCollectionSelector = connect(
    NoteCollectionSelector,
    map_state_to_props,
    map_dispatch_to_props)
