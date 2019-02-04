from nose2.tools import such
from nete.gtkgui.reducers.ui import reduce
from nete.gtkgui.state.models import Ui
from nete.gtkgui.actions.action_types import ActionType


with such.A('reduce') as it:
    @it.has_setup
    def setup():
        it.state = Ui(
            current_note_collection_id='d9c1b608-ba78-4061-9192-d0e81fffeb69',
            is_editing_title=False,
            is_editing_text=False,
            paned_position=200,
            filter_term_entry_focus=False)

    @it.should('reset is_editing_* flags on')
    def test():
        it.state = it.state.update({
            'is_editing_title': True,
        })

        result = reduce(it.state, {
            'type': ActionType.SELECT_NOTE,
            'title': 'OTHER NOTE',
        })

        it.assertEqual(result['is_editing_title'], False)
