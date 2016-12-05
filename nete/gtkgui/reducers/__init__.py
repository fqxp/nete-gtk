from .cache import cache_reduce
from .current_note import current_note_reduce
from .ui_state import ui_state_reduce

from flurx import combine_reducers


reducers = {
    'current_note': current_note_reduce,
    'ui_state': ui_state_reduce,
    'cache': cache_reduce,
}

reduce_action = combine_reducers(reducers)
