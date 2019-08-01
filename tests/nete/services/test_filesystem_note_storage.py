import pytest

from gi.repository import Gio

from nete.services.filesystem_note_storage import FilesystemNoteStorage
from nete.gui.state.models import Note, NoteCollection


__doc__ = 'FilesystemNoteStorage'


@pytest.fixture
def note_collection(tmp_path):
    return NoteCollection(
        id='93e16575-472b-4d8f-8b42-a7668725650b',
        name='NAME',
        directory=str(tmp_path),
    )


@pytest.fixture
def note_storage(note_collection):
    return FilesystemNoteStorage(note_collection)


@pytest.fixture
def create_note(tmp_path):
    def create_note(title):
        open(tmp_path.joinpath('{}.md'.format(title)), 'w').write('TEXT')
    return create_note


def test__list__returns_list_of_note_list_items(note_storage, create_note):
    create_note('NOTE 1')
    create_note('NOTE 2')
    create_note('NOTE 3')

    result = note_storage.list()

    assert len(result) == 3
    assert sorted([note['title'] for note in result]) == ['NOTE 1', 'NOTE 2', 'NOTE 3']


def test__create_note__creates_a_note_in_filesystem(
    note_collection,
    note_storage,
    tmp_path
):
    note = note_storage.create_note()

    assert tmp_path.joinpath('{}.md'.format(note.title)).exists()
    assert note['note_collection_id'] == note_collection.id


def test__load__returns_note_from_filesystem(note_storage, create_note):
    create_note('NOTE 1')

    result = note_storage.load('NOTE 1')

    assert result['text'] == 'TEXT'


def test__save__saves_note_to_filesystem(note_storage, tmp_path):
    note = Note(
        note_collection_id=note_storage.note_collection.id,
        title='NOTE 1',
        text='TEXT',
        cursor_position=0,
        needs_save=False,
    )

    note_storage.save(note)

    assert open(tmp_path.joinpath('NOTE 1.md')).read() == 'TEXT'


def test__move_to_trash__moves_note_from_folder_to_trash(
    note_storage,
    tmp_path,
    create_note
):
    create_note('NOTE 1')

    assert tmp_path.joinpath('NOTE 1.md').exists()

    note_storage.move_to_trash('NOTE 1')

    assert not tmp_path.joinpath('NOTE 1.md').exists()
    assert Gio.File.new_for_uri('trash:///NOTE 1.md').query_exists()


def test__move__renames_note(note_storage, tmp_path, create_note):
    create_note('NOTE 1')

    assert tmp_path.joinpath('NOTE 1.md').exists()
    assert not tmp_path.joinpath('NOTE 2.md').exists()

    note_storage.move('NOTE 1', 'NOTE 2')

    assert not tmp_path.joinpath('NOTE 1.md').exists()
    assert tmp_path.joinpath('NOTE 2.md').exists()


def test__validate_note_title__returns_no_error_if_title_unchanged(note_storage):
    assert note_storage.validate_note_title('TITLE', 'TITLE') is None


def test__validate_note_title__returns_error_if_title_empty(note_storage):
    assert note_storage.validate_note_title('', 'NOTE 1') is not None


def test__validate_note_title__returns_error_if_title_too_long(note_storage):
    assert note_storage.validate_note_title('x' * 253, 'NOTE 1') is not None


def test__validate_note_title__returns_error_if_title_contains_slash(note_storage):
    assert note_storage.validate_note_title('a/b', 'NOTE 1') is not None


def test__validate_note_title__returns_error_if_new_title_exists(
    note_storage,
    create_note
):
    create_note('NEW TITLE')

    assert note_storage.validate_note_title('NEW TITLE', 'NOTE 1') is not None
