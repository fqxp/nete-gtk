from pyrsistent import (
    PClass,
    PRecord,
    field,
    pvector_field,
)


class NoteCollection(PClass):
    id = field(type=str, mandatory=True)
    name = field(type=str, mandatory=True)
    directory = field(type=str, mandatory=True)


class Note(PRecord):
    note_collection_id = field(type=str, mandatory=True)
    title = field(type=(str, type(None)), mandatory=True)
    text = field(type=(str, type(None)), mandatory=True)
    needs_save = field(type=bool, mandatory=True)
    cursor_position = field(type=int, mandatory=True)


class NoteListItem(PRecord):
    title = field(type=(str, type(None)), mandatory=True)
    visible = field(type=bool, mandatory=True)


class NoteList(PRecord):
    notes = pvector_field(NoteListItem)
    filter_term = field(type=str, mandatory=True)
    preselected_note_title = field(type=(str, type(None)), mandatory=True)


class Ui(PRecord):
    paned_position = field(type=int)
    current_note_collection_id = field(
        type=(str, type(None)),
        mandatory=True)
    focus = field(type=(str, type(None)),
                  invariant=lambda value: (
                      value in (
                          None,
                          'note_view',
                          'note_editor',
                          'note_title_editor',
                          'filter_term_entry',
                          'note_collection_selector',
                      ), None)
                  )
    title_error_message = field(type=(str, type(None)))


class Configuration(PClass):
    note_collections = pvector_field(NoteCollection)


class State(PRecord):
    note_list = field(type=NoteList)
    current_note = field(type=(Note, type(None)))
    configuration = field(type=(Configuration, type(None)))
    ui = field(type=Ui)
    development_mode = field(type=bool)
