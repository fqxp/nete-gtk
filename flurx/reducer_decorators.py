from pyrsistent import thaw
from .call_reducer import call_reducer
import traceback


__all__ = [
    'debug_reducer',
]


def debug_reducer(print_diff=False, print_traceback=False):
    from termcolor import cprint, colored

    def decorator(reducer):
        def decorator_inner(state, action):
            print()
            print(
                colored('→ %s' % action['type'].value, 'magenta'))
            cprint('before: %s' % _wrap_dict(thaw(state)), 'blue')
            cprint('action: %s' % _wrap_dict(action), 'yellow')
            new_state = call_reducer(reducer, state, action)
            cprint('after:  %s' % _wrap_dict(thaw(new_state)), 'green')

            if print_diff:
                import deepdiff
                diff = deepdiff.DeepDiff(thaw(old_state), thaw(new_state))
                print('  diff: %r' % diff)

            if print_traceback:
                traceback.print_stack()

            return new_state

        return decorator_inner
    return decorator


def _wrap_dict(d):
    from pprint import pformat
    return ('\n' + ' ' * 8).join(pformat(d, width=80).split('\n'))
