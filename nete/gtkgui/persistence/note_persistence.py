from gi.repository import GObject
from fluous.gobject import connect
from nete.services.storage_factory import create_storage


def map_state_to_props(state):
    return (
        ('storage_uri', state['ui_state']['storage_uri']),
        ('note', {
            'id': state['ui_state']['current_note_id'],
            'title': state['current_note']['note_title'],
            'text': state['current_note']['note_text'],
        }),
    )


class NotePersistence(GObject.GObject):
    storage_uri = GObject.property(type=str)
    note = GObject.property(type=GObject.TYPE_PYOBJECT)

    def __init__(self):
        super().__init__()
        self._current_note_id = None
        self._connect_events()

    def _connect_events(self):
        self.connect('notify::note', lambda source, param: self._save_note())

    def _save_note(self):
        if self._current_note_id != self.get_property('note')['id']:
            self._current_note_id = self.get_property('note')['id']
            return

        storage = create_storage(self.get_property('storage_uri'))
        storage.save(self.get_property('note'))

    def _build_note(self):
        return {
            'id': self.get_property('note_idd'),
            'title': self.get_property('note_title'),
            'text': self.get_property('note_text'),
        }


ConnectedNotePersistence = connect(NotePersistence, map_state_to_props)
