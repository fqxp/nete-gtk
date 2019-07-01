from nete.gtkgui.state.models import Note, NoteListItem
from nete.gtkgui.state.utils.note_list import is_visible
import datetime
import glob
import logging
import os
import os.path

logger = logging.getLogger(__name__)


class FilesystemNoteStorage(object):

    def __init__(self, note_collection):
        self._note_collection = note_collection
        logger.debug('Using directory {}'.format(self.note_dir()))

    def list(self, filter_term=None):
        return [
            NoteListItem(
                title=title,
                visible=is_visible(title, filter_term))
            for title in self._list_entries()]

    def create_note(self):
        note = Note(
            note_collection_id=self._note_collection.id,
            title=self._find_title('New Note'),
            text='',
            cursor_position=0,
            needs_save=False,
        )

        self.save(note)

        return note

    def load(self, note_title):
        with open(self._filename_from_title(note_title)) as fd:
            content = fd.read()
            return Note(
                note_collection_id=self._note_collection.id,
                title=note_title,
                text=content,
                cursor_position=0,
                needs_save=False,
            )

    def save(self, note):
        self._ensure_dir_exists(self.note_dir())

        if note.get('title') is None:
            raise Exception('Cannot save note - title is not set')
        if note.get('text') is None:
            raise Exception('Cannot save note - text is not set')

        filename = self._filename_from_title(note['title'])
        logger.debug('Saving note in {}'.format(filename))

        with open(filename, 'w') as fd:
            fd.write(note['text'])

    def delete(self, note_title):
        logger.debug('Deleting note {}'.format(note_title))
        os.unlink(self._filename_from_title(note_title))

    def move(self, old_title, new_title):
        old_filename = self._filename_from_title(old_title)
        new_filename = self._filename_from_title(new_title)

        if os.path.exists(new_filename):
            raise Exception(
                'Cannot rename note »{}«'
                'because target title »{}« exists'.format(
                    old_filename, new_filename))

        os.rename(old_filename, new_filename)

    def note_dir(self):
        return self._note_collection.directory

    def _list_entries(self):
        entries = [
            self._title_from_filename(os.path.basename(filename))
            for filename in glob.glob(os.path.join(self.note_dir(), '*.md'))
        ]
        return entries

    def _ensure_dir_exists(self, note_dir):
        if not os.path.isdir(note_dir):
            os.makedirs(note_dir)

    def _filename_from_title(self, title):
        return os.path.join(self.note_dir(), '%s.md' % title)

    def _title_from_filename(self, filename):
        title, extension = os.path.splitext(os.path.basename(filename))
        return title

    def _find_title(self, prefix):
        return '{} {}'.format(prefix, datetime.datetime.now())
