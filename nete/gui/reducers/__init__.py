from fluous.functions import combine_reducers
from nete.gui.reducers import current_note, ui, note_list, configuration


reducer = combine_reducers({
    'current_note': current_note.reduce,
    'ui': ui.reduce,
    'note_list': note_list.reduce,
    'configuration': configuration.reduce,
})
