from nete.gtkgui.state.models import (
    Note,
    NoteCollection,
    NoteList,
    NoteListItem,
    State,
    Ui,
)
from nete.gtkgui.state import selectors
import unittest


class SelectorsTestCase(unittest.TestCase):

    def setUp(self):
        self.state = State(
            note_collections={
                'NOTE-COLLECTION-ID': NoteCollection(
                    id='NOTE-COLLECTION-ID',
                    name='NAME',
                    directory='/tmp',
                ),
            },
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
            development_mode=True,
        )

    def test_current_note_collection(self):
        result = selectors.current_note_collection(self.state)

        self.assertIsInstance(result, NoteCollection)

    def test_current_note_returns_current_note(self):
        result = selectors.current_note(self.state)

        self.assertIsInstance(result, Note)
        self.assertEqual(result['title'], 'NOTE 1')

    def test_visible_notes_returns_only_visible_notes(self):
        state = self.state.transform(
            ('note_list', 'notes', 1, 'visible'),
            False)

        result = selectors.visible_notes(state)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'NOTE 1')

    def test_note_list_first_returns_first_note_list_item(self):
        result = selectors.note_list_first(self.state)

        self.assertEqual(result['title'], 'NOTE 1')

    def test_note_list_first_returns_none_for_empty_note_list(self):
        state = self.state.transform(('note_list', 'notes'), [])

        result = selectors.note_list_first(state)

        self.assertIsNone(result)

    def test_note_list_last_returns_last_note_list_item(self):
        result = selectors.note_list_last(self.state)

        self.assertEqual(result['title'], 'NOTE 2')

    def test_note_list_last_returns_none_for_empty_note_list(self):
        state = self.state.transform(('note_list', 'notes'), [])

        result = selectors.note_list_last(state)

        self.assertIsNone(result)

    def test_note_list_contains_returns_true_if_note_is_contained(self):
        result = selectors.note_list_contains(self.state, 'NOTE 1')

        self.assertTrue(result)

    def test_note_list_contains_returns_true_if_note_is_contained(self):
        result = selectors.note_list_contains(self.state, 'NOTE 3')

        self.assertFalse(result)

    def test_note_list_next_returns_next_note_title_matching_title(self):
        result = selectors.note_list_next(self.state, 'NOTE 1')

        self.assertEqual(result, 'NOTE 2')

    def test_note_list_next_returns_none_if_title_is_last(self):
        result = selectors.note_list_next(self.state, 'NOTE 2')

        self.assertIsNone(result)

    def test_note_list_previous_returns_previous_note_title_matching_title(self):
        result = selectors.note_list_previous(self.state, 'NOTE 2')

        self.assertEqual(result, 'NOTE 1')

    def test_note_list_previous_returns_none_if_title_is_last(self):
        result = selectors.note_list_previous(self.state, 'NOTE 1')

        self.assertIsNone(result)
