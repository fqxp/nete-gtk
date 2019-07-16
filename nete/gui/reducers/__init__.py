from fluous.functions import combine_reducers
from . import current_note, ui, note_list


reducer = combine_reducers({
    'current_note': current_note.reduce,
    'ui': ui.reduce,
    'note_list': note_list.reduce,
})
