from nete.services.storage_factory import create_storage
from immutable import ImmutableDict


class NotePersistence:

    def __init__(self, store):
        self.storage_uri = None
        self.storage = None
        self.note_last_seen = None

        store.subscribe(self.set_state)
        self.set_state(store.state)

    def set_state(self, state):
        if state['current_note_id'] is None:
            return

        if self.storage != state['storage_uri']:
            self.storage_uri = state['storage_uri']
            self.storage = create_storage(self.storage_uri)

        note = self._build_note_from_state(state)
        if ((self.note_last_seen is None or note['id'] == self.note_last_seen['id'])
                and self.note_last_seen != note):
            self.storage.save(dict(note))

        self.note_last_seen = note

    def _build_note_from_state(self, state):
        return ImmutableDict({
            'id': state['current_note_id'],
            'title': state['note_title'],
            'text': state['note_text'],
        })
