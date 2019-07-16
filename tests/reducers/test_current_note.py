from nete.gui.reducers.current_note import reduce
from nete.gui.state.models import Note
from nete.gui.actions.action_types import ActionType
import unittest


class ReduceTestCase(unittest.TestCase):

    def setUp(self):
        self.state = Note(
            title='TITLE',
            text='TEXT',
            needs_save=False,
            note_collection_id='NOTE-COLLECTION-ID',
            cursor_position=0
        )

    def test_reduce_changes_current_note_on_select_note_action(self):
        result = reduce(self.state, {
            'type': ActionType.SELECT_NOTE,
            'note': Note(
                title='OTHER TITLE',
                text='OTHER TEXT',
                needs_save=True,
                note_collection_id='NOTE-COLLECTION-ID',
                cursor_position=0
            )})

        self.assertEqual(result['title'], 'OTHER TITLE')
        self.assertEqual(result['text'], 'OTHER TEXT')
        self.assertEqual(result['needs_save'], True)

    def test_reduce_changes_note_text_on_change_note_text_action(self):
        result = reduce(self.state, {
            'type': ActionType.CHANGE_NOTE_TEXT,
            'text': 'NEW TEXT',
        })

        self.assertEqual(result['text'], 'NEW TEXT')

    def test_reduce_changes_note_title_on_change_note_title_action(self):
        result = reduce(self.state, {
            'type': ActionType.FINISH_EDIT_NOTE_TITLE,
            'new_title': 'NEW TITLE',
        })

        self.assertEqual(result['title'], 'NEW TITLE')

    def test_reduce_switches_needs_save_to_false_on_note_saved_action(self):
        result = reduce(self.state, {
            'type': ActionType.NOTE_SAVED,
            'needs_save': True,
        })

        self.assertEqual(result['needs_save'], False)
