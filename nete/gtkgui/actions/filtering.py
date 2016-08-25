from nete.gtkgui.actions.action_types import ActionType
from nete.services.storage_factory import create_storage


def set_filter_term_entry_focus(has_focus):
    return {
        'type': ActionType.FOCUS_FILTER_TERM_ENTRY,
        'has_focus': has_focus,
    }

def change_filter_term(filter_term):
    def change_filter_term(dispatch, state):
        storage = create_storage(state['ui_state']['storage_uri'])
        return {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': filter_term,
            'filtered_notes': storage.list(filter_term),
        }
    return change_filter_term
