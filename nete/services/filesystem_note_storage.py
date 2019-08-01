import datetime
import glob
import logging
import os
import os.path
from typing import List, Union

from gi.repository import Gio

from nete.gui.state.models import Note, NoteCollection, NoteListItem
from nete.gui.state.utils.note_list import is_visible
from nete.gui.state.selectors import current_note


class FilesystemNoteStorage:

    SUFFIX = '.md'

    def __init__(self, note_collection: NoteCollection):
        self.note_collection = note_collection

    def list(self) -> List[NoteListItem]:
        return [
            NoteListItem(
                title=title,
                visible=True
            ) for title in self._list_entries()]

    def create_note(self) -> Note:
        note = Note(
            note_collection_id=self.note_collection.id,
            title=self._find_title('New Note'),
            text='',
            cursor_position=0,
            needs_save=False,
        )

        self.save(note)

        return note

    def load(self, note_title: str) -> Note:
        with open(self._filename_from_title(note_title)) as fd:
            content = fd.read()
            return Note(
                note_collection_id=self.note_collection.id,
                title=note_title,
                text=content,
                cursor_position=0,
                needs_save=False,
            )

    def save(self, note: Note):
        self._ensure_dir_exists(self.note_dir())

        if note.get('title') is None:
            raise Exception('Cannot save note - title is not set')
        if note.get('text') is None:
            raise Exception('Cannot save note - text is not set')

        filename = self._filename_from_title(note['title'])

        with open(filename, 'w') as fd:
            fd.write(note['text'])

    def move_to_trash(self, note_title: str):
        Gio.File.new_for_path(self._filename_from_title(note_title)).trash()

    def move(self, old_title, new_title):
        old_filename = self._filename_from_title(old_title)
        new_filename = self._filename_from_title(new_title)

        if os.path.exists(new_filename):
            raise Exception(
                'Cannot rename note »{}«'
                'because target title »{}« exists'.format(
                    old_filename, new_filename))

        os.rename(old_filename, new_filename)

    def note_dir(self) -> str:
        return self.note_collection.directory

    def validate_note_title(
        self,
        title: str,
        current_title: str
    ) -> Union[str, None]:
        if title == current_title:
            return None
        elif title == '':
            return 'Note title cannot be empty'
        elif len(title) > self._maximum_filename_length():
            return 'Note title can not be longer than {} characters'.format(
                self._maximum_filename_length())
        elif '/' in title:
            return 'Note title may not contain the letter »/«'
        elif self._exists(title):
            return 'There already is a note with that title'

        return None

    def _exists(self, note_title: str) -> bool:
        return os.path.exists(self._filename_from_title(note_title))

    def _maximum_filename_length(self) -> int:
        return os.statvfs(self.note_dir()).f_namemax - len(self.SUFFIX)

    def _list_entries(self) -> List[str]:
        entries = [
            self._title_from_filename(os.path.basename(filename))
            for filename in glob.glob(os.path.join(self.note_dir(),
                                                   '*{}'.format(self.SUFFIX)))
        ]
        return entries

    def _ensure_dir_exists(self, note_dir: str):
        if not os.path.isdir(note_dir):
            os.makedirs(note_dir)

    def _filename_from_title(self, title: str) -> str:
        return os.path.join(self.note_dir(), '{}{}'.format(title, self.SUFFIX))

    def _title_from_filename(self, filename: str) -> str:
        title, suffix = os.path.splitext(os.path.basename(filename))
        return title

    def _find_title(self, prefix: str) -> str:
        return '{} {}'.format(prefix, datetime.datetime.now())
