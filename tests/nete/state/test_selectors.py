import pytest
from pyrsistent import s

from nete.state.models import (
    Configuration,
    Note,
    NoteCollection,
    NoteList,
    NoteListItem,
    State,
    Ui,
)
from nete.state import selectors


@pytest.fixture
def state():
    return State(
        note_list=NoteList(
            notes=[
                NoteListItem(
                    title='NOTE 1',
                    visible=True,
                ),
                NoteListItem(
                    title='NOTE 2',
                    visible=True,
                ),
            ],
            filter_term='',
            preselected_note_title=None,
        ),
        current_note=Note(
            note_collection_id='NOTE-COLLECTION-ID',
            title='NOTE 1',
            text='TEXT',
            needs_save=False,
            cursor_position=0,
        ),
        ui=Ui(
            current_note_collection_id='NOTE-COLLECTION-ID',
            focus=None,
            paned_position=250,
        ),
        configuration=Configuration(
            note_collections=s(
                NoteCollection(
                    id='NOTE-COLLECTION-ID',
                    name='NAME',
                    directory='/tmp',
                ),
            ),
        ),
        development_mode=True,
    )


def test__current_note_collection__returns_current_note_collection(state):
    """ current_note_collection returns current note collection """
    result = selectors.current_note_collection(state)

    assert isinstance(result, NoteCollection)


def test__current_note__returns_current_note(state):
    result = selectors.current_note(state)

    assert isinstance(result, Note)
    assert result['title'] == 'NOTE 1'


def test__visible_notes__returns_only_visible_notes(state):
    state = state.transform(
        ('note_list', 'notes', 1, 'visible'),
        False)

    result = selectors.visible_notes(state)

    assert len(result) == 1
    assert result[0].title == 'NOTE 1'


def test__note_list_first__returns_first_note_list_item(state):
    result = selectors.note_list_first(state)

    assert result['title'] == 'NOTE 1'


def test__note_list_first__returns_none_for_empty_note_list(state):
    state = state.transform(('note_list', 'notes'), [])

    result = selectors.note_list_first(state)

    assert result is None


def test__note_list_last__returns_last_note_list_item(state):
    result = selectors.note_list_last(state)

    assert result['title'] == 'NOTE 2'


def test__note_list_last__returns_none_for_empty_note_list(state):
    state = state.transform(('note_list', 'notes'), [])

    result = selectors.note_list_last(state)

    assert result is None


def test__note_list_contains__returns_true_if_note_is_contained(state):
    result = selectors.note_list_contains(state, 'NOTE 1')

    assert result is True


def test__note_list_contains__returns_false_if_note_is_not_contained(state):
    result = selectors.note_list_contains(state, 'NOTE 3')

    assert result is False


def test__note_list_next__returns_next_note_title_matching_title(state):
    result = selectors.note_list_next(state, 'NOTE 1')

    assert result == 'NOTE 2'


def test__note_list_next__returns_none_if_title_is_last(state):
    result = selectors.note_list_next(state, 'NOTE 2')

    assert result is None


def test__note_list_previous__returns_previous_note_title_matching_title(state):
    result = selectors.note_list_previous(state, 'NOTE 2')

    assert result == 'NOTE 1'


def test__note_list_previous__returns_none_if_title_is_last(state):
    result = selectors.note_list_previous(state, 'NOTE 1')

    assert result is None
