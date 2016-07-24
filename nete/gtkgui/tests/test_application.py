from nete.gtkgui.application import reducer
from nete.gtkgui.state.action_types import *
from immutable import make_immutable
from nose2.tools import such
import mock


with such.A('reducer') as it:

    @it.has_setup
    def setup():
        it.state = make_immutable({
            'storage_uri': 'nete:notes',
            'is_editing_title': False,
            'is_editing_text': False,
            'note_title': None,
            'note_text': None,
            'notes': [],
            'ui_state': {
                'current_note_id': None,
                'window_position': None,
                'window_size': [600, 400],
                'paned_position': 120,
            },
        })

    @it.should('should update the UI state on LOADED_UI_STATE action')
    def test():
        result = reducer(it.state, {
            'type': LOADED_UI_STATE,
            'ui_state': {
                'current_note_id': 'NEW-ID',
                'paned_position': 222,
            }
        })

        it.assertEqual(result['ui_state']['current_note_id'], 'NEW-ID')
        it.assertEqual(result['ui_state']['paned_position'], 222)

    @it.should('change the window position and size on MOVE_OR_RESIZE_WINDOW action')
    def test():
        result = reducer(it.state, {
            'type': MOVE_OR_RESIZE_WINDOW,
            'position': [100, 100],
            'size': [300, 300],
        })

        it.assertEqual(result['ui_state']['window_position'], make_immutable([100, 100]))
        it.assertEqual(result['ui_state']['window_size'], make_immutable([300, 300]))

    @it.should('change the paned position on MOVE_PANED_POSITION action')
    def test():
        result = reducer(it.state, {
            'type': MOVE_PANED_POSITION,
            'position': 666,
        })

        it.assertEqual(result['ui_state']['paned_position'], 666)

    it.createTests(globals())
