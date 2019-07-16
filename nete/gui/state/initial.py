from nete.gui.state.models import NoteList, Ui, State, NoteCollection
from nete.utils import in_development_mode


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
        preselected_note_title=None,
        ),
    current_note=None,
    ui=Ui(
        current_note_collection_id='630415b9-290e-4b3e-94d3-c96bca7b9694',
        focus=None,
        paned_position=250,
        ),
    development_mode=in_development_mode(),
    )
