from nete.services.storage_factory import create_storage
from immutable import ImmutableDict


class NotePersistence:

    def __init__(self, store):
        self.storage_uri = None
        self.storage = None
        self.note_hash = None

        store.subscribe(self.set_state)
        self.set_state(store.state)

    def set_state(self, state):
        if self.storage != state['storage_uri']:
            self.storage_uri = state['storage_uri']
            self.storage = create_storage(self.storage_uri)

        note = self._make_note(state)
        note_hash = hash(note)
        if state['current_note_id'] is not None and self.note_hash != note_hash:
            self.storage.save(dict(note))
            self.note_hash = note_hash

    def _make_note(self, state):
        return ImmutableDict({
            'id': state['current_note_id'],
            'title': state['note_title'],
            'text': state['note_text'],
        })
