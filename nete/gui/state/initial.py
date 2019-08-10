from nete.gui.state.models import (
    NoteList,
    State,
    Ui,
)
from nete.utils import in_development_mode


initial_state = State(
    note_list=NoteList(
        notes=[],
        filter_term='',
        preselected_note_title=None,
    ),
    current_note=None,
    configuration=None,
    ui=Ui(
        current_note_collection_id=None,
        focus=None,
        paned_position=250,
        title_error_message=None,
        info_message=None,
        zoom_level=1.0,
    ),
    development_mode=in_development_mode(),
)
