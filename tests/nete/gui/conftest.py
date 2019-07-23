import pytest
import re

from nete.gui.state.models import (
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


def pytest_itemcollected(item):
    parent = item.parent.obj
    node = item.obj
    prefix = '{} [{}]'.format(
        parent.__doc__.strip() if parent.__doc__ else parent.__class__.__name__,
        node.__module__
    )
    suffix = node.__doc__.strip() if node.__doc__ else format_description(node.__name__)
    if prefix or suffix:
        item._nodeid = ' '.join((prefix, suffix))


def format_description(test_function_name):
    fn_name_without_prefix = re.sub(r'^test_+', '', test_function_name)
    parts = fn_name_without_prefix.split('__', 1)
    if len(parts) == 1:
        return parts[0]

    return '{} {}'.format(
        parts[0],
        parts[1].replace('_', ' ')
    )
