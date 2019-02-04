from nete.services.filesystem_note_storage import FilesystemNoteStorage


def create_storage(note_collection):
    return FilesystemNoteStorage(note_collection)
