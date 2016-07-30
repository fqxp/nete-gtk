from __future__ import print_function
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
            self._id_from_filename(os.path.basename(filename))
            for filename in glob.glob(os.path.join(self.note_dir(), '*.json'))
        ]

        return notes

    def load(self, note_id):
        with open(self._filename_from_id(note_id)) as fd:
            content = json.load(fd)
            return {
                'id': note_id,
                'title': content['title'],
                'text': content['text'],
            }

    def save(self, note):
        self._ensure_dir_exists(self.note_dir())

        if note.get('id') is None:
            raise Exception('Cannot save note - note has no id')
        if note.get('title') is None:
            raise Exception('Cannot save note - title is not set')
        if note.get('text') is None:
            raise Exception('Cannot save note - text is not set')

        filename = self._filename_from_id(note['id'])
        print('Saving note in %s' % filename)

        with open(filename, 'w') as fd:
            content = {
                'id': note['id'],
                'title': note['title'],
                'text': note['text'],
            }
            json.dump(content, fd)

    def delete(self, note_id):
        print('Deleting note %s' % (note_id,))
        os.unlink(self._filename_from_id(note_id))

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

