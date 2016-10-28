from nete.gtkgui.actions.action_types import ActionType
from nete.services.note_storage import create_storage
from flurx import action


@action
def set_filter_term_entry_focus(has_focus):
    return {
        'type': ActionType.FOCUS_FILTER_TERM_ENTRY,
        'has_focus': has_focus,
    }


@action
def change_filter_term(filter_term):
    def change_filter_term(state):
        storage = create_storage(state['ui_state']['storage_uri'])
        return {
            'type': ActionType.CHANGE_FILTER_TERM,
            'filter_term': filter_term,
            'filtered_notes': storage.list(filter_term),
        }

    return change_filter_term
