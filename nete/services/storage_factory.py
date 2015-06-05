from nete.services.filesystem_note_storage import FilesystemNoteStorage


class StorageFactory(object):

    @classmethod
    def create_storage(cls, nete_uri):
        #import pdb ; pdb.set_trace()
        return FilesystemNoteStorage(nete_uri.context)

