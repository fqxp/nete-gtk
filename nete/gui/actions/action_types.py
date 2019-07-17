from enum import Enum


class ActionType(Enum):
    SELECT_NOTE = 'SELECT_NOTE'
    CREATED_NOTE = 'CREATED_NOTE'
    DELETE_NOTE = 'DELETE_NOTE'

    TOGGLE_EDIT_NOTE_TEXT = 'TOGGLE_EDIT_NOTE_TEXT'
    CHANGE_NOTE_TEXT = 'CHANGE_NOTE_TEXT'
    CHANGE_CURSOR_POSITION = 'CHANGE_CURSOR_POSITION'
    FINISH_EDIT_NOTE_TEXT = 'FINISH_EDIT_NOTE_TEXT'

    TOGGLE_EDIT_NOTE_TITLE = 'TOGGLE_EDIT_NOTE_TITLE'
    FINISH_EDIT_NOTE_TITLE = 'FINISH_EDIT_NOTE_TITLE'
    CANCEL_EDIT_NOTE_TITLE = 'CANCEL_EDIT_NOTE_TITLE'

    FOCUS_FILTER_TERM_ENTRY = 'FOCUS_FILTER_TERM_ENTRY'
    CHANGE_FILTER_TERM = 'CHANGE_FILTER_TERM'

    LOADED_NOTES = 'LOADED_NOTES'
    LOADED_UI_STATE = 'LOADED_UI_STATE'

    SELECT_FIRST = 'SELECT_FIRST'
    SELECT_NEXT = 'SELECT_NEXT'
    SELECT_PREVIOUS = 'SELECT_PREVIOUS'

    PRESELECT_NOTE = 'PRESELECT_NOTE'

    NOTE_LOADED = 'NOTE_LOADED'
    NOTE_SAVED = 'NOTE_SAVED'

    MOVE_PANED_POSITION = 'MOVE_PANED_POSITION'

    LOAD_CONFIGURATION = 'LOAD_CONFIGURATION'
    SAVE_CONFIGURATION = 'SAVE_CONFIGURATION'
