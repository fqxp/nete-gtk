from nete.gui.actions.action_types import ActionType


def change_filter_term(filter_term):
    return {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': filter_term,
    }
