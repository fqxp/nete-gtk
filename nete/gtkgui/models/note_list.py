from gi.repository import Gtk, GObject
from nete.models.nete_uri import NeteUri
from nete.services.storage_factory import StorageFactory
from .note import Note


class NoteList(Gtk.ListStore):
    nete_uri = GObject.property(type=str)

    def __init__(self, nete_uri):
        super().__init__(Note, str)
        self.note_storage = StorageFactory.create_storage(NeteUri(nete_uri))

    def load(self):
        self.clear()
        for note in map(Note, self.note_storage.list()):
            self.append((note, note.note.title))

