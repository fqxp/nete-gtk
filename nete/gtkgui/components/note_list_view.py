from gi.repository import Gtk, GObject, Pango
from nete.gtkgui.state.actions import select_note
from fluous.gobject import connect


NOTE_ID = 0
NOTE_TITLE = 1


class NoteListModel(Gtk.ListStore):
    nete_uri = GObject.property(type=str)

    def __init__(self):
        super().__init__(str, str)

    def set_data(self, notes):
        self.clear()

        for note in notes:
            row = [note['id'], note['title']]
            self.append(row)

    def update(self, note_list):
        notes_by_id = dict((note['id'], note) for note in note_list)

        self._delete_rows(notes_by_id)
        self._update_rows(notes_by_id)
        self._append_rows(note_list)
        self._sync_order(note_list)

    def _delete_rows(self, notes_by_id):
        rows_to_delete = [
            row
            for row in self
            if row[NOTE_ID] not in notes_by_id]

        for row in rows_to_delete:
            self.remove(row.iter)

    def _update_rows(self, notes_by_id):
        for row in self:
            note = notes_by_id[row[NOTE_ID]]
            row[NOTE_TITLE] = note['title']

    def _append_rows(self, note_list):
        row_ids = [row[NOTE_ID] for row in self]
        rows_to_append = [
            (note['id'], note['title'])
            for note in note_list
            if note['id'] not in row_ids]

        for row in rows_to_append:
            self.append(row)

    def _sync_order(self, note_list):
        row_ids = [row[NOTE_ID] for row in self]
        new_order = [
            row_ids.index(note['id'])
            for note in note_list]

        self.reorder(new_order)

    def get_treeiter_by_note_id(self, note_id):
        tree_iter = self.get_iter_first()

        while tree_iter is not None:
            if self[tree_iter][NOTE_ID] == note_id:
                return tree_iter
            tree_iter = self.iter_next(tree_iter)

        raise Exception('note with id %s not found' % note_id)

    def get_tree_path_by_note(self, note_id):
        treeiter = self.get_treeiter_by_note_id(note_id)
        return self.get_path(treeiter)


def map_state_to_props(state):
    return (
        ('notes', state['notes']),
        ('current-note', state['ui_state']['current_note_id']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'selected-note': lambda note_id: dispatch(select_note(note_id)),
    }


class NoteListView(Gtk.Grid):

    notes = GObject.property(type=GObject.TYPE_PYOBJECT)
    current_note = GObject.property(type=str, default='')

    __gsignals__ = {
        'selected-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str,)),
    }

    def __init__(self):
        super().__init__()

        self.set_name('note-list-view')

        self._build_ui()
        self._connect_events()

    def _connect_events(self):
        self.connect(
            'notify::notes',
            lambda source, param: self._on_notify_notes())
        self.connect(
            'notify::current-note',
            lambda source, param: self._on_notify_current_note())
        self._changed_selection_handler = self.tree_view.get_selection().connect(
            'changed',
            lambda selection: self.emit(
                'selected-note', self._selected_note_id(selection)))

    def _on_notify_notes(self):
        self._list_model().update(self.get_property('notes'))
        self._scroll_current_cell_into_view()

    def _on_notify_current_note(self):
        if self.get_property('current-note') is None:
            return

        with self.tree_view.get_selection().handler_block(self._changed_selection_handler):
            self._select_note(self.get_property('current-note'))

    def _select_note(self, note_id):
        treeiter = self._list_model().get_treeiter_by_note_id(note_id)
        self.tree_view.get_selection().select_iter(treeiter)
        self._scroll_current_cell_into_view()

    def _selected_note_id(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is None:
            return None
        return model[treeiter][0]

    def _list_model(self):
        return self.tree_view.get_model()

    def _build_ui(self):
        model = NoteListModel()

        self.scrollable_treelist = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True,
            can_focus=False)
        self.attach(self.scrollable_treelist, 0, 0, 1, 1)

        self.tree_view = Gtk.TreeView(model, headers_visible=False, can_focus=False)
        title_renderer = Gtk.CellRendererText()
        title_renderer.set_property('ellipsize', Pango.EllipsizeMode.END)
        column = Gtk.TreeViewColumn('title', title_renderer, text=1)
        self.tree_view.append_column(column)

        self.scrollable_treelist.add(self.tree_view)

    def _scroll_current_cell_into_view(self):
        note_id = self.get_property('current-note')

        if note_id:
            self.tree_view.scroll_to_cell(
                self._list_model().get_tree_path_by_note(note_id))


ConnectedNoteListView = connect(NoteListView, map_state_to_props, map_dispatch_to_props)