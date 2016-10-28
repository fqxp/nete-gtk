from nete.services.filesystem_note_storage import FilesystemNoteStorage
from nete.models.nete_uri import NeteUri
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers=1)


def save_note(note):
    def save_note():
        note_to_save = {
            'id': note['id'],
            'title': note['title'],
            'text': note['text'],
            'cursor_position': note['cursor_position'],
        }
        storage = create_storage(note['storage_uri'])
        storage.save(note_to_save)

    return executor.submit(save_note)


def create_storage(nete_uri):
    nete_uri = NeteUri(nete_uri)
    return FilesystemNoteStorage(nete_uri.context)
