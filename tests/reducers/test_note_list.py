from nete.gui.reducers.note_list import reduce
from nete.gui.state.models import NoteList, NoteListItem, Note
from nete.gui.actions.action_types import ActionType
import unittest


class NoteListTestCase(unittest.TestCase):

    def setUp(self):
        self.state = NoteList(
            filter_term='',
            notes=[
                NoteListItem(title='FOO', visible=True),
                NoteListItem(title='BAR', visible=True),
            ],
            preselected_note_title=None,
        )
        self.note = Note(
            note_collection_id='NOTE COLLECTION ID',
            title='TITLE',
            text='TEXT',
            needs_save=False,
            cursor_position=0
        )

    def test_adds_an_empty_note_on_created_note_action(self):
        result = reduce(self.state, {
            'type': ActionType.CREATED_NOTE,
            'note': self.note,
        })

        titles = sorted(note['title'] for note in result['notes'])
        self.assertEqual(titles, ['BAR', 'FOO', 'TITLE'])

    def test_sets_visibility_according_to_current_filter_on_created_note_action(self):
        state = self.state.set('filter_term', 'FO')
        result = reduce(state, {
            'type': ActionType.CREATED_NOTE,
            'note': self.note,
        })

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        self.assertNotIn('TITLE', titles)

    def test_deletes_note_on_deleted_note_action(self):
        result = reduce(self.state, {
            'type': ActionType.DELETE_NOTE,
            'note_title': 'FOO'
        })

        self.assertEqual(len(result['notes']), 1)
        self.assertEqual(result['notes'][0]['title'], 'BAR')

    def test_changes_note_title_on_finish_edit_note_title_action(self):
        result = reduce(self.state, {
            'type': ActionType.FINISH_EDIT_NOTE_TITLE,
            'old_title': 'FOO',
            'new_title': 'NEW TITLE',
        })

        titles = sorted(note['title'] for note in result['notes'])
        self.assertEqual(titles, ['BAR', 'NEW TITLE'])

    def test_sets_filter_term_on_change_filter_term_action(self):
        result = reduce(self.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        self.assertEqual(result['filter_term'], 'FO')

    def test_filters_notes_on_change_filter_term_action(self):
        result = reduce(self.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        self.assertEqual(titles, ['FOO'])

    def test_preselect_first_visible_note_on_change_filter_term_action(self):
        self.state.set('preselected_note_title', None)
        result = reduce(self.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        self.assertEqual(result['preselected_note_title'], 'FOO')

    def test_doesnt_preselect_if_currently_preselected_note_visible(self):
        self.state.set('preselected_note_title', 'FOO')
        result = reduce(self.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'FO',
        })

        self.assertEqual(result['preselected_note_title'], 'FOO')

    def test_preselects_first_visible_note_if_current_one_not_visible(self):
        result = reduce(self.state, {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': 'BA',
        })

        self.assertEqual(result['preselected_note_title'], 'BAR')

    def test_sets_the_note_list_on_loaded_notes_action(self):
        result = reduce(self.state, {
            'type': ActionType.LOADED_NOTES,
            'notes': [
                NoteListItem(title='NEW NOTE 1', visible=True),
                NoteListItem(title='NEW NOTE 2', visible=True),
            ]})

        titles = sorted(note['title']
                        for note in result['notes']
                        if note['visible'])
        self.assertEqual(titles, ['NEW NOTE 1', 'NEW NOTE 2'])
