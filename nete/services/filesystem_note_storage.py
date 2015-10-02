from __future__ import print_function
from nete.models.note import Note
import glob
import json
import os
import os.path
import uuid


class FilesystemNoteStorage(object):

    def __init__(self, context):
        self._context = context
        print('Using directory %s' % self.note_dir())

    def list(self):
        notes = [
            self.load(self._id_from_filename(os.path.basename(filename)))
            for filename in glob.glob(os.path.join(self.note_dir(), '*.json'))
        ]

        return notes

    def load(self, note_id):
        note = self.create()
        note.id = note_id

        with open(self._filename_from_id(note_id)) as fd:
            content = json.load(fd)
            note.title = content['title']
            note.text = content['text']

        return note

    def save(self, note):
        self._ensure_dir_exists(self.note_dir())

        if note.id is None:
            note.id = str(uuid.uuid4())

        filename = self._filename_from_id(note.id)
        print("Saving note %s in %s" % (note.id, filename))

        with open(filename, 'w') as fd:
            content = {
                'title': note.title,
                'text': note.text,
            }
            json.dump(content, fd)

    def create(self):
        return Note(storage=self)

    def delete(self, note):
        os.unlink(self._filename_from_id(note.id))

    def note_dir(self):
        if 'NETE_DIR' in os.environ:
            basedir = os.environ['NETE_DIR']
        elif 'XDG_DATA_HOME' in os.environ:
            basedir = os.path.join(os.environ['XDG_DATA_HOME'], 'nete')
        else:
            basedir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'nete')

        return os.path.join(basedir, self._context)

    def _ensure_dir_exists(self, note_dir):
        if not os.path.isdir(note_dir):
            os.makedirs(note_dir)

    def _filename_from_id(self, id):
        return os.path.join(self.note_dir(), '%s.json' % id)

    def _id_from_filename(self, filename):
        return os.path.splitext(os.path.basename(filename))[0]

