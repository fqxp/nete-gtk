from nete.gtkgui.application import initial_state
from nete.gtkgui.reducers import reducer
from nete.gtkgui.actions.action_types import ActionType
from pyrsistent import freeze
import unittest


class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.state = freeze(initial_state)

    def test_reducer_updates_ui_state_on_loaded_ui_state_action(self):
        result = reducer(self.state, {
            'type': ActionType.LOADED_UI_STATE,
            'ui': {
                'paned_position': 222,
            }
        })

        self.assertEqual(result['ui']['paned_position'], 222)

    def test_reducer_changes_paned_position_on_move_paned_position_action(self):
        result = reducer(self.state, {
            'type': ActionType.MOVE_PANED_POSITION,
            'position': 666,
        })

        self.assertEqual(result['ui']['paned_position'], 666)
