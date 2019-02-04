from nete.utils import in_development_mode
from .models import NoteList, Note, Ui, State, NoteCollection


initial_state = State(
    note_collections={
        '630415b9-290e-4b3e-94d3-c96bca7b9694': NoteCollection(
            id='630415b9-290e-4b3e-94d3-c96bca7b9694',
            name='Personal',
            directory='/home/frank/devel/nete/markdown-notes/notes',
            ),
    },
    note_list=NoteList(
        notes=[],
        filter_term='',
        ),
    current_note=None,
    ui=Ui(
        current_note_collection_id='630415b9-290e-4b3e-94d3-c96bca7b9694',
        is_editing_title=False,
        is_editing_text=False,
        paned_position=250,
        filter_term_entry_focus=False,
        ),
    development_mode=in_development_mode(),
    )
