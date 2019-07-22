from pyrsistent import thaw
from .functions import call_reducer
import traceback

__all__ = (
    'debug_reducer',
)


def debug_reducer(print_state=True, print_diff=False, print_traceback=False):
    from termcolor import cprint, colored

    def decorator(reducer):
        count = 1

        def decorator_inner(state, action):
            nonlocal count

            print()
            print(
                colored('→ {}'.format(action['type'].value), 'magenta'),
                colored('#{}'.format(count), 'white', attrs=['dark'])
            )
            if print_state:
                cprint('before: {}'.format(_wrap_dict(thaw(state))), 'blue')
            cprint('action: {}'.format(_wrap_dict(action)), 'yellow')

            new_state = call_reducer(reducer, state, action)

            if print_state:
                cprint('after:  {}'.format(_wrap_dict(thaw(new_state))), 'green')

            if print_diff:
                import deepdiff
                diff = deepdiff.DeepDiff(thaw(state), thaw(new_state))
                print('  diff: {}'.format(_wrap_dict(diff)))

            if print_traceback:
                traceback.print_stack()

            count += 1

            return new_state

        return decorator_inner
    return decorator


def _wrap_dict(d):
    from pprint import pformat
    return ('\n' + ' ' * 8).join(pformat(d, width=80).split('\n'))
