from gi.repository import Gtk, GObject, Pango
from nete.gtkgui.actions import select_note, create_note
from .filter_view import ConnectedFilterView
from fluous.gobject import connect


class NoteListView(Gtk.Grid):

    notes = GObject.property(type=GObject.TYPE_PYOBJECT)
    current_note_title = GObject.property(type=str, default='')

    __gsignals__ = {
        'selected-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str,)),
        'create-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, ()),
    }

    def __init__(self, build_component, **kwargs):
        super().__init__(**kwargs)

        self.set_name('note-list-view')

        self._build_ui(build_component)
        self._connect_events()
        self._on_notify_notes()

    def _connect_events(self):
        self.connect(
            'notify::notes',
            lambda source, param: self._on_notify_notes())
        self.connect(
            'notify::current-note-title',
            lambda source, param:
                self._select_note(source.get_property('current-note-title')))
        self._changed_selection_handler = self.tree_view.get_selection().connect(
            'changed',
            lambda selection:
                self.emit('selected-note', self._selected_note_title(selection)))
        self.create_button.connect(
            'clicked',
            lambda source: self.emit('create-note'))

    def _on_notify_notes(self):
        self._list_model().update(self.get_property('notes'))
        self._select_note(self.get_property('current-note-title'))

    def _select_note(self, note_title):
        if note_title is None:
            return
        treeiter = self._list_model().get_treeiter_by_note_title(note_title)
        if treeiter is None:
            return

        with self.tree_view.get_selection().handler_block(self._changed_selection_handler):
            self.tree_view.get_selection().select_iter(treeiter)
        self._scroll_current_cell_into_view(treeiter)

    def _selected_note_title(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is None:
            return None
        return model[treeiter][model.COLUMN_NOTE_TITLE]

    def _list_model(self):
        return self.tree_view.get_model()

    def _build_ui(self, build_component):
        filter_view = build_component(ConnectedFilterView)
        self.attach(filter_view, 0, 0, 1, 1)

        model = NoteListModel()

        self.scrollable_treelist = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True,
            can_focus=False)
        self.attach(self.scrollable_treelist, 0, 1, 1, 1)

        self.tree_view = Gtk.TreeView(
            model,
            headers_visible=False,
            can_focus=True)
        title_renderer = Gtk.CellRendererText(
            ellipsize=Pango.EllipsizeMode.END
        )
        column = Gtk.TreeViewColumn('title', title_renderer, markup=model.COLUMN_NOTE_TITLE)
        self.tree_view.append_column(column)

        self.scrollable_treelist.add(self.tree_view)

        self.create_button = Gtk.Button('New Note')
        self.attach(self.create_button, 0, 2, 1, 1)

        self.set_focus_chain([])

    def _scroll_current_cell_into_view(self, treeiter):
        tree_path = self._list_model().get_path(treeiter)
        self.tree_view.scroll_to_cell(tree_path)


class NoteListModel(Gtk.ListStore):

    COLUMN_NOTE_TITLE = 0

    def __init__(self):
        super().__init__(str)

    def update(self, note_list):
        visible_note_list = [note
                     for note in note_list
                     if note['visible']]
        notes_by_title = {note['title']: note
                          for note in visible_note_list}

        self._delete_rows(notes_by_title)
        self._update_rows(notes_by_title)
        self._append_rows(visible_note_list)
        self._sync_order(visible_note_list)

    def _delete_rows(self, notes_by_title):
        rows_to_delete = [
            row
            for row in self
            if row[self.COLUMN_NOTE_TITLE] not in notes_by_title]

        for row in rows_to_delete:
            self.remove(row.iter)

    def _update_rows(self, notes_by_title):
        for row in self:
            note = notes_by_title[row[self.COLUMN_NOTE_TITLE]]
            row[self.COLUMN_NOTE_TITLE] = note['title']

    def _append_rows(self, note_list):
        row_titles = [row[self.COLUMN_NOTE_TITLE] for row in self]
        rows_to_append = [
            (note['title'],)
            for note in note_list
            if note['title'] not in row_titles
        ]

        for row in rows_to_append:
            self.append(row)

    def _sync_order(self, note_list):
        row_titles = [row[self.COLUMN_NOTE_TITLE] for row in self]
        new_order = [
            row_titles.index(note['title'])
            for note in note_list
        ]

        self.reorder(new_order)

    def get_treeiter_by_note_title(self, note_title):
        tree_iter = self.get_iter_first()

        while tree_iter is not None:
            if self[tree_iter][self.COLUMN_NOTE_TITLE] == note_title:
                return tree_iter
            tree_iter = self.iter_next(tree_iter)

        return None


def map_state_to_props(state):
    return (
        ('notes', state['note_list']['notes']),
        ('current-note-title', state['current_note']['title'] if state['current_note'] else None),
    )


def map_dispatch_to_props(dispatch):
    return {
        'selected-note': lambda source, note_id: dispatch(select_note(note_id)),
        'create-note': lambda source: dispatch(create_note()),
    }


ConnectedNoteListView = connect(NoteListView, map_state_to_props, map_dispatch_to_props)
