from .functions import call_reducer
import traceback


__all__ = [
    'log_action',
    'log_state_diff',
    'log_state',
    'log_traceback']


def log_action(reducer):
    def logging_reducer(state, action):
        new_state = call_reducer(reducer, state, action)

        print('ACTION <%s>: %r' % (action['type'], action))

        return new_state
    return logging_reducer


def log_state_diff(reducer):
    def log_state_reducer(state, action):
        new_state = call_reducer(reducer, state, action)

        print_diff(state, new_state)

        return new_state
    return log_state_reducer


def log_state(reducer):
    def log_state_reducer(state, action):
        new_state = call_reducer(reducer, state, action)

        print(new_state)

        return new_state
    return log_state_reducer


def log_traceback(reducer):
    def traceback_reducer(state, action):
        new_state = call_reducer(reducer, state, action)

        traceback.print_stack()

        return new_state
    return traceback_reducer


def print_diff(old_state, new_state):
    import deepdiff
    diff = deepdiff.DeepDiff(old_state.mutable(), new_state.mutable())

    if len(diff) == 0:
        print('*** NO CHANGES')
        return

    print('*** CHANGES')
    for change_type, changes in diff.items():
        if change_type in ('type_changes', 'values_changed'):
            for key in sorted(changes.keys()):
                change_detail = changes[key]
                print('    %s: %r -> %r' % (key, change_detail['oldvalue'], change_detail['newvalue']))
        elif change_type == 'iterable_item_added':
            for key in sorted(changes.keys()):
                print('    +++ %s: %r' % (key, changes[key]))
        else:
            print('*** UNKNOWN CHANGE TYPE: %s' % change_type)
            print('    %r' % changes)
    print('***')
