import pytest

from nete.state.models import (
    Configuration,
    NoteCollection,
    NoteList,
    State,
    Ui,
)


@pytest.fixture
def initial_state():
    return State(
        note_list=NoteList(
            notes=[],
            filter_term='',
            preselected_note_title=None,
        ),
        current_note=None,
        configuration=Configuration(
            note_collections=[
                NoteCollection(
                    id='ee913522-a50a-4c81-a931-afe4c8c7598f',
                    name='COLLECTION 1',
                    directory='/tmp/note_collection_1',
                ),
                NoteCollection(
                    id='e32ccaa4-6021-41fc-9d2a-2b534cf77ad1',
                    name='COLLECTION 2',
                    directory='/tmp/note_collection_2',
                ),
            ],
        ),
        ui=Ui(
            current_note_collection_id='ee913522-a50a-4c81-a931-afe4c8c7598f',
            focus=None,
            paned_position=250,
        ),
        development_mode=True,
    )
