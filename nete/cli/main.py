#! /usr/bin/env python2.7
# coding: utf-8

from nete.services.filesystem_note_storage import FilesystemNoteStorage
import sys


class CommandLineClient(object):

    def __init__(self):
        self._storage = FilesystemNoteStorage('./notes')

    def run(self, argv):
        cmd = argv[1] if len(argv) > 1 else ''

        if cmd == 'list':
            self.list()
        elif cmd == 'view':
            self.view(argv[2])
        else:
            self.usage()

    def usage(self):
        print '''Available commands:
list        List available notes
view ID     View note starting with given ID
'''

    def list(self):
        notes = self._storage.list()
        for note in notes:
            print('* %s: %s (%d bytes)' % (note.id, note.title, len(note.text)))

        print('%d notes in total' % len(notes))

    def view(self, note_id):
        note = self._find_by_id(note_id)

        print( '''
Id:    %(id)s
Title: %(title)s
Text:
%(text)s''' % {
            'id': note.id,
            'title': note.title,
            'text': note.text,
        }).strip()

    def _find_by_id(self, note_id):
        matching_notes = [note
                          for note in self._storage.list()
                          if note.id.startswith(note_id)]
        if len(matching_notes) > 1:
            raise Exception('id is ambiguous')
        elif len(matching_notes) == 0:
            raise Exception('id doesn‘t exist')

        return matching_notes[0]


def main():
    CommandLineClient().run(sys.argv)

