from functools import lru_cache
from typing import List, Union

from nete.gui.state.models import (
    Note,
    NoteCollection,
    NoteListItem,
    State,
    Ui,
)


@lru_cache()
def current_note_collection(state: State) -> NoteCollection:
    current_note_collection_id = state['ui']['current_note_collection_id']
    return state['note_collections'][current_note_collection_id]


@lru_cache()
def current_note(state: State) -> Union[Note, None]:
    return state.get('current_note')


@lru_cache()
def visible_notes(state: State) -> List[NoteListItem]:
    return [
        note_list_item
        for note_list_item in state['note_list']['notes']
        if note_list_item['visible']
    ]


@lru_cache()
def note_list_first(state: State) -> Union[Note, None]:
    notes = visible_notes(state)
    return notes[0] if len(notes) > 0 else None


@lru_cache()
def note_list_last(state: State) -> Union[Note, None]:
    notes = visible_notes(state)
    return notes[-1] if len(notes) > 0 else None


@lru_cache()
def note_list_contains(state: State, note_title: str) -> bool:
    notes = visible_notes(state)
    return any(note['title'] == note_title for note in notes)


@lru_cache()
def note_list_next(state: State, note_title: str) -> Union[Note, None]:
    notes = visible_notes(state)
    for i, note in enumerate(notes):
        if note['title'] == note_title:
            return notes[i + 1]['title'] if i + 1 < len(notes) else None
    return None


@lru_cache()
def note_list_previous(
        state: State,
        current_note_title: str
        ) -> Union[Note, None]:
    notes = visible_notes(state)
    for i, note in enumerate(notes):
        if note['title'] == current_note_title:
            return notes[i - 1]['title'] if i > 0 else None
    return None


@lru_cache()
def ui_state(state: State) -> Ui:
    return state['ui']
