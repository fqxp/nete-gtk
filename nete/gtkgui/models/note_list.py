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
            note.connect('changed', self.on_note_changed)
            self.append((note, note.title))

    def on_note_changed(self, note):
        treeiter = self._get_treeiter_for_note(note)
        self[treeiter] = (note, note.title)

    def _get_treeiter_for_note(self, note):
        treeiter = self.get_iter_first()

        while treeiter is not None:
            if self[treeiter][0] == note:
                return treeiter
            treeiter = self.iter_next(treeiter)

        raise Exception('note not found')
