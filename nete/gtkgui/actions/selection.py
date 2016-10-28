from flurx import action
from .action_types import ActionType
from nete.services.note_storage import create_storage
from nete.gtkgui.state import note_list
import uuid


@action
def load_note(note_id):
    if note_id is None:
        return

    def do_load_note(state):
        storage = create_storage(state['ui_state']['storage_uri'])
        loaded_note(storage.load(note_id))

    return do_load_note


@action
def loaded_note(note):
    return {
        'type': ActionType.LOADED_NOTE,
        'id': note['id'],
        'title': note['title'],
        'text': note['text'],
        'cursor_position': note['cursor_position'],
    }


@action
def create_note():
    return {
        'type': ActionType.CREATE_NOTE,
        'id': str(uuid.uuid4()),
        'title': 'New Note',
        'text': '',
    }


@action
def next_note():
    def do_next_note(state):
        notes = state['cache']['notes']
        current_note_id = state['ui_state']['current_note_id']

        if current_note_id is None or not note_list.contains(notes, current_note_id):
            select_first()

        next_note_id = note_list.next_note_id(notes, current_note_id)
        if next_note_id:
            return load_note(next_note_id)

    return do_next_note


@action
def prev_note():
    def do_prev_note(state):
        notes = state['cache']['notes']
        current_note_id = state['ui_state']['current_note_id']

        if current_note_id is None or not note_list.contains(notes, current_note_id):
            select_last()

        previous_note_id = note_list.previous_note_id(notes, current_note_id)
        if previous_note_id is not None:
            return load_note(previous_note_id)

    return do_prev_note


@action
def select_first():
    def select_first(state):
        first_note_id = note_list.first_note_id(state['cache']['notes'])
        if first_note_id is not None:
            load_note(first_note_id)

    return select_first


@action
def select_last():
    def select_last(state):
        last_note_id = note_list.last_note_id(state['cache']['notes'])
        if last_note_id is not None:
            load_note(last_note_id)

    return select_last
