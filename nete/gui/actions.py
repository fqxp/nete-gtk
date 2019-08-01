from nete.gui.action_types import ActionType
from nete.services import ui_state_storage
from nete.gui.services import config_storage
from nete.gui.state.selectors import (
    current_note,
    current_note_collection,
    note_collection_by_id,
    note_list_contains,
    note_list_first,
    note_list_last,
    note_list_next,
    note_list_previous,
    visible_notes,
)
from nete.services.storage_factory import create_storage


def cancel_edit_note_title():
    return {
        'type': ActionType.CANCEL_EDIT_NOTE_TITLE,
    }


def change_cursor_position(cursor_position):
    return {
        'type': ActionType.CHANGE_CURSOR_POSITION,
        'cursor_position': cursor_position,
    }


def change_filter_term(filter_term):
    return {
        'type': ActionType.CHANGE_FILTER_TERM,
        'filter_term': filter_term,
    }


def change_note_text(text):
    return {
        'type': ActionType.CHANGE_NOTE_TEXT,
        'text': text,
    }


def choose_preselected_note():
    def choose_preselected_note(dispatch, state):
        preselected_note_title = state['note_list']['preselected_note_title']

        if preselected_note_title is None:
            return

        return select_note(preselected_note_title)

    return choose_preselected_note


def close_note():
    return {
        'type': ActionType.CLOSE_NOTE,
    }


def create_note():
    def create_note(dispatch, state):
        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        note = storage.create_note()

        dispatch(created_note(note))
        dispatch(select_note(note['title']))
        dispatch(toggle_edit_note_title())

    return create_note


def created_note(note):
    return {
        'type': ActionType.CREATED_NOTE,
        'note': note,
    }


def move_note_to_trash():
    def move_note_to_trash(dispatch, state):
        if current_note(state) is None:
            return

        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        current_note_title = current_note(state)['title']
        next_note_title = (
            note_list_next(state, current_note_title)
            or note_list_previous(state, current_note_title)
            or None
        )
        dispatch(select_note(next_note_title))

        storage.move_to_trash(current_note_title)

        return {
            'type': ActionType.MOVE_NOTE_TO_TRASH,
            'note_title': current_note_title,
        }
    return move_note_to_trash


def finish_edit_note_text(note_id):
    return {
        'type': ActionType.FINISH_EDIT_NOTE_TEXT,
    }


def finish_edit_note_title(new_title):
    def finish_edit_note_title(dispatch, state):
        if current_note(state) is None:
            return

        old_title = current_note(state)['title']

        if old_title == new_title:
            return cancel_edit_note_title()

        storage = create_storage(current_note_collection(state))
        storage.move(old_title, new_title)

        return {
            'type': ActionType.FINISH_EDIT_NOTE_TITLE,
            'old_title': old_title,
            'new_title': new_title,
        }

    return finish_edit_note_title


def focus(widget_name):
    return {
        'type': ActionType.FOCUS,
        'widget_name': widget_name,
    }


def initialize():
    def initialize(dispatch, state):
        note_collection = current_note_collection(state)
        dispatch(select_collection(note_collection.id))
    return initialize


def load_configuration():
    def load_configuration(dispatch, state):
        configuration = config_storage.load_configuration()

        return {
            'type': ActionType.LOAD_CONFIGURATION,
            'configuration': configuration,
        }
    return load_configuration


def load_ui_state():
    def load_ui_state(dispatch, state):
        try:
            ui_state = ui_state_storage.load_ui_state()
            dispatch(loaded_ui_state(ui_state))
        except FileNotFoundError:
            dispatch(select_first())

    return load_ui_state


def loaded_ui_state(ui_state):
    def loaded_ui_state(dispatch, state):
        return {
            'type': ActionType.LOADED_UI_STATE,
            'ui': ui_state,
        }
    return loaded_ui_state


def move_paned_position(position):
    return {
        'type': ActionType.MOVE_PANED_POSITION,
        'position': position,
    }


def preselect_next():
    def preselect_next(dispatch, state):
        if len(state['note_list']['notes']) is None:
            return

        preselected_note_title = state['note_list']['preselected_note_title']
        if preselected_note_title is None:
            return preselect_note(visible_notes(state)[0]['title'])

        next_note_title = note_list_next(state, preselected_note_title)
        if next_note_title is not None:
            return preselect_note(next_note_title)

    return preselect_next


def preselect_note(title):
    return {
        'type': ActionType.PRESELECT_NOTE,
        'note_title': title,
    }


def preselect_previous():
    def preselect_previous(dispatch, state):
        if len(state['note_list']['notes']) is None:
            return

        preselected_note_title = state['note_list']['preselected_note_title']
        if preselected_note_title is None:
            return preselect_note(visible_notes(state)[-1]['title'])

        previous_note_title = note_list_previous(state, preselected_note_title)
        if previous_note_title is not None:
            return preselect_note(previous_note_title)

    return preselect_previous


def reset():
    return {
        'type': ActionType.RESET,
    }


def save_configuration():
    def save_configuration(dispatch, state):
        config_storage.save_configuration(state['configuration'])
    return save_configuration


def save_note(note):
    def save_note(dispatch, state):
        if note is None or not note['needs_save']:
            return

        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        storage.save(note)
        dispatch(saved_note())

    return save_note


def saved_note():
    return {
        'type': ActionType.NOTE_SAVED,
    }


def save_ui_state(ui_state):
    ui_state_storage.save_ui_state(ui_state)


def select_collection(collection_id):
    def select_collection(dispatch, state):
        note_collection = note_collection_by_id(state, collection_id)
        storage = create_storage(note_collection)
        dispatch({
            'type': ActionType.SELECT_NOTE_COLLECTION,
            'collection_id': collection_id,
            'notes': storage.list(),
        })
    return select_collection


def select_first():
    def select_first(dispatch, state):
        first_note_title = note_list_first(state)['title']

        if first_note_title is None:
            return

        return select_note(first_note_title)

    return select_first


def select_none():
    return {
        'type': ActionType.SELECT_NOTE,
        'note': None,
    }


def select_note(note_title):
    if note_title is None:
        return

    def select_note(dispatch, state):
        storage = create_storage(current_note_collection(state))
        note = storage.load(note_title)

        dispatch({
            'type': ActionType.SELECT_NOTE,
            'note': note,
        })

    return select_note


def select_last():
    def select_last(dispatch, state):
        last_note_title = note_list_last(state)
        if last_note_title is None:
            return

        return select_note(last_note_title)

    return select_last


def select_next():
    def select_next(dispatch, state):
        note = current_note(state)
        if note is None:
            return select_first()

        current_note_title = note['title']

        if not note_list_contains(state, current_note_title):
            return select_first()

        next_note_title = note_list_next(state, current_note_title)
        if next_note_title:
            return select_note(next_note_title)

    return select_next


def select_previous():
    def select_previous(dispatch, state):
        note = current_note(state)
        if note is None:
            return select_last()

        current_note_title = note['title']

        if not note_list_contains(state, current_note_title):
            return select_last()

        previous_note_title = note_list_previous(state, current_note_title)
        if previous_note_title is not None:
            return select_note(previous_note_title)

    return select_previous


def toggle_edit_note_text():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TEXT,
    }


def toggle_edit_note_title():
    return {
        'type': ActionType.TOGGLE_EDIT_NOTE_TITLE,
    }


def validate_note_title(transient_title):
    def validate_note_title(dispatch, state):
        note_collection = current_note_collection(state)
        storage = create_storage(note_collection)
        error_message = storage.validate_note_title(
            transient_title,
            state['current_note']['title']
        )

        return {
            'type': ActionType.VALIDATE_NOTE_TITLE,
            'error_message': error_message,
        }

    return validate_note_title
