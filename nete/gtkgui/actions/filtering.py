from nete.gtkgui.actions.action_types import ActionType


def set_filter_term_entry_focus(has_focus):
    return {
        'type': ActionType.FOCUS_FILTER_TERM_ENTRY,
        'has_focus': has_focus,
    }


def change_filter_term(filter_term):
    return {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': filter_term,
    }
