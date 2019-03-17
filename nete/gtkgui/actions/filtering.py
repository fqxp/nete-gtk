from nete.gtkgui.actions.action_types import ActionType


def focus_filter_term_entry():
    return {
        'type': ActionType.FOCUS_FILTER_TERM_ENTRY,
    }


def change_filter_term(filter_term):
    return {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': filter_term,
    }
