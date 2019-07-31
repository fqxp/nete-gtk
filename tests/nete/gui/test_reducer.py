import pytest

from nete.gui.reducer import reduce
from nete.gui.state.models import (
    Note,
    NoteListItem,
)
from nete.gui.action_types import ActionType


@pytest.fixture
def state(initial_state):
    return initial_state


@pytest.fixture
def state_with_notes(state):
    return state.transform(
        ['current_note'],
        Note(
            note_collection_id=state['ui']['current_note_collection_id'],
            title='FOO',
            text='TEXT',
            needs_save=False,
            cursor_position=0,
        ),

        ['note_list', 'notes'],
        [
            NoteListItem(title='FOO', visible=True),
            NoteListItem(title='BAR', visible=True),
        ],
    )


@pytest.fixture
def note():
    return Note(
        note_collection_id='NOTE COLLECTION ID',
        title='TITLE',
        text='TEXT',
        needs_save=False,
        cursor_position=0
    )


def test__CREATED_NOTE__adds_an_empty_note(state_with_notes, note):
    result = reduce(state_with_notes, {
        'type': ActionType.CREATED_NOTE,
        'note': note,
    })

    titles = sorted(note['title'] for note in result['note_list']['notes'])
    assert titles == ['BAR', 'FOO', 'TITLE']


def test__CREATED_NOTE__sets_visibility_according_to_current_filter(state, note):
    state = state.transform(['note_list', 'filter_term'], 'FO')
    result = reduce(state, {
        'type': ActionType.CREATED_NOTE,
        'note': note,
    })

    titles = sorted(note['title']
                    for note in result['note_list']['notes']
                    if note['visible'])
    assert 'TITLE' not in titles


def test__DELETE_NOTE__deletes_note(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.DELETE_NOTE,
        'note_title': 'FOO'
    })

    assert len(result['note_list']['notes']) == 1
    assert result['note_list']['notes'][0]['title'] == 'BAR'


def test__FINISH_EDIT_NOTE_TITLE__changes_note_title(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.FINISH_EDIT_NOTE_TITLE,
        'old_title': 'FOO',
        'new_title': 'NEW TITLE',
    })

    titles = sorted(note['title'] for note in result['note_list']['notes'])
    assert titles == ['BAR', 'NEW TITLE']


def test__CHANGE_FILTER_TERM__sets_filter_term(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': 'FO',
    })

    assert result['note_list']['filter_term'] == 'FO'


def test__CHANGE_FILTER_TERM__filters_notes(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': 'FO',
    })

    titles = sorted(note['title']
                    for note in result['note_list']['notes']
                    if note['visible'])
    assert titles == ['FOO']


def test__CHANGE_FILTER_TERM__preselects_first_visible_note(state_with_notes):
    state_with_notes.transform(['note_list', 'preselected_note_title'], None)
    result = reduce(state_with_notes, {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': 'FO',
    })

    assert result['note_list']['preselected_note_title'] == 'FOO'


def test__CHANGE_FILTER_TERM__doesnt_preselect_if_preselected_visible(state_with_notes):
    state = state_with_notes.transform(
        ['note_list', 'preselected_note_title'], 'FOO')

    result = reduce(state, {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': 'FO',
    })

    assert result['note_list']['preselected_note_title'] == 'FOO'


def test__CHANGE_FILTER_TERM__preselects_first_visible_note_if_current_not_visible(state_with_notes):  # noqa
    ''' CHANGE_FILTER_TERM preselects first visible note if current note isn’t visible'''
    result = reduce(state_with_notes, {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': 'BA',
    })

    assert result['note_list']['preselected_note_title'] == 'BAR'


def test__SELECT_NOTE__reduce_changes_current_note(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.SELECT_NOTE,
        'note': Note(
            title='OTHER TITLE',
            text='OTHER TEXT',
            needs_save=True,
            note_collection_id='NOTE-COLLECTION-ID',
            cursor_position=0
        )})

    assert result['current_note'].title == 'OTHER TITLE'
    assert result['current_note'].text == 'OTHER TEXT'
    assert result['current_note'].needs_save is True


def test__CHANGE_NOTE_TEXT__reduce_changes_note_text(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'text': 'NEW TEXT',
    })

    assert result['current_note']['text'] == 'NEW TEXT'


def test__FINISH_EDIT_NOTE_TITLE__reduce_changes_note_title(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.FINISH_EDIT_NOTE_TITLE,
        'new_title': 'NEW TITLE',
        'old_title': state_with_notes['current_note']['title'],
    })

    assert result['current_note']['title'] == 'NEW TITLE'


def test__NOTE_SAVED__reduce_switches_needs_save_to_false(state_with_notes):
    result = reduce(state_with_notes, {
        'type': ActionType.NOTE_SAVED,
        'needs_save': True,
    })

    assert result['current_note']['needs_save'] is False
