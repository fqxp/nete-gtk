from gi.repository import Gtk, GObject
from fluous.gobject import connect

from nete.gui.actions.ui import select_collection


class HeaderBar(Gtk.HeaderBar):

    current_note_collection_id = GObject.Property(type=str)
    note_collections = GObject.Property(type=GObject.TYPE_PYOBJECT)

    __gsignals__ = {
        'collection-selected':
            (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.set_show_close_button(True)

        self.collection_chooser = Gtk.ComboBoxText()
        for i, note_collection in enumerate(self.note_collections):
            self.collection_chooser.append(
                note_collection.id,
                note_collection.name
            )
            if self.current_note_collection_id == note_collection.id:
                self.collection_chooser.set_property('active', i)
        self.pack_start(self.collection_chooser)

    def _connect_events(self):
        self.bind_property(
            'current_note_collection_id',
            self.collection_chooser,
            'active-id',
            GObject.BindingFlags.DEFAULT)

        self.collection_chooser.connect(
            'changed',
            lambda source: self.emit(
                'collection-selected', source.get_active_id()))


def map_state_to_props(state):
    note_title = (state['current_note']['title']
                  if state['current_note']
                  else 'No note loaded')
    return (
        ('title', '%s (nete%s)' % (
            note_title, '-DEVELOPMENT' if state['development_mode'] else '',
        )),
        ('note_collections',
         sorted(
             state['configuration'].note_collections,
             key=lambda collection: collection.name
         )),
        ('current_note_collection_id',
            state['ui']['current_note_collection_id']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'collection-selected': lambda source, collection_id:
            dispatch(select_collection(collection_id)),
    }


ConnectedHeaderBar = connect(
    HeaderBar,
    map_state_to_props,
    map_dispatch_to_props)
