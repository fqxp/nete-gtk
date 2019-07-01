from pyrsistent import PRecord, field, pmap_field, pvector_field


class NoteCollection(PRecord):
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
    current_note_collection_id = field(type=str)
    focus = field(type=(str, type(None)),
                  invariant=lambda value: (
                      value in (
                          None,
                          'note_view',
                          'note_editor',
                          'note_title_editor',
                          'filter_term'
                      ), None)
                  )


class State(PRecord):
    note_collections = pmap_field(str, NoteCollection)
    note_list = field(type=NoteList)
    current_note = field(type=(Note, type(None)))
    ui = field(type=Ui)
    development_mode = field(type=bool)
