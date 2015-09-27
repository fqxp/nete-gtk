#! /usr/bin/env python3

from nete.services.filesystem_note_storage import FilesystemNoteStorage
import sys
import random

words = list(map(str.strip, open('/usr/share/dict/ngerman').readlines()))

def random_text(count=1):
    return ' '.join([
        words[random.randint(0, len(words)-1)]
        for i in range(count)
    ]).capitalize()


if __name__ == '__main__':
    count = int(sys.argv[1])
    storage = FilesystemNoteStorage('./notes')

    for i in range(count):
        print('Creating note #%d' % i)
        note = storage.create()
        note.title = random_text(2)
        note.text = random_text(50)
        storage.save(note)

