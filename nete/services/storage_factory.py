from nete.services.filesystem_note_storage import FilesystemNoteStorage
from nete.models.nete_uri import NeteUri


def create_storage(nete_uri):
    nete_uri = NeteUri(nete_uri)
    return FilesystemNoteStorage(nete_uri.context)

