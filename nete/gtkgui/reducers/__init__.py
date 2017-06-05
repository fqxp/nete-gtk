from fluous.functions import combine_reducers
from . import current_note, ui_state, cache


reducer = combine_reducers({
    'current_note': current_note.reduce,
    'ui_state': ui_state.reduce,
    'cache': cache.reduce,
})

