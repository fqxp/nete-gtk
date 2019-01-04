from nete.gtkgui.application import reducer, initial_state
from nete.gtkgui.actions.action_types import ActionType
from pyrsistent import freeze
from nose2.tools import such


with such.A('reducer') as it:

    @it.has_setup
    def setup():
        it.state = freeze(initial_state)

    @it.should('should update the UI state on LOADED_UI_STATE action')
    def test():
        result = reducer(it.state, {
            'type': ActionType.LOADED_UI_STATE,
            'ui_state': {
                'current_note_id': 'NEW-ID',
                'paned_position': 222,
            }
        })

        it.assertEqual(result['ui_state']['current_note_id'], 'NEW-ID')
        it.assertEqual(result['ui_state']['paned_position'], 222)

    @it.should('change the paned position on MOVE_PANED_POSITION action')
    def test():
        result = reducer(it.state, {
            'type': ActionType.MOVE_PANED_POSITION,
            'position': 666,
        })

        it.assertEqual(result['ui_state']['paned_position'], 666)

    it.createTests(globals())
