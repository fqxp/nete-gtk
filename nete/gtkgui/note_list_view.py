from gi.repository import Gtk, GObject, Pango
from nete.gtkgui.state.actions import select_note


NOTE_ID = 0
NOTE_TITLE = 1


class NoteListModel(Gtk.ListStore):
    nete_uri = GObject.property(type=str)

    def __init__(self):
        super().__init__(str, str)

        self.set_sort_column_id(NOTE_TITLE, Gtk.SortType.ASCENDING)

    def set_data(self, notes):
        self.clear()

        for note_id, note in notes.items():
            row = [note_id, note['title']]
            self.append(row)

    def update(self, notes):
        note_ids = tuple(row[NOTE_ID] for row in self)
        deleted_row_ids = []

        for row in self:
            if row[NOTE_ID] in notes:
                title = notes[row[NOTE_ID]]['title']
                if row[NOTE_TITLE] != title:
                    row[NOTE_TITLE] = title
            else:
                deleted_row_ids.append(row)

        for deleted_row_id in deleted_row_ids:
            self.remove(deleted_row_id.iter)

        for note_id, note in notes.items():
            if note_id not in note_ids:
                row = [note_id, note['title']]
                self.append(row)

    def get_note_id_by_treeiter(self, treeiter):
        return self[tree_iter][0]

    def get_treeiter_by_note_id(self, note_id):
        tree_iter = self.get_iter_first()

        while tree_iter is not None:
            if self[tree_iter][NOTE_ID] == note_id:
                return tree_iter
            tree_iter = self.iter_next(tree_iter)

        raise Exception('note not found')

    def get_tree_path_by_note(self, note_id):
        treeiter = self.get_treeiter_by_note_id(note_id)
        return self.get_path(treeiter)


class NoteListView(Gtk.Grid):

    notes = GObject.property(type=GObject.TYPE_PYOBJECT)
    current_note = GObject.property(type=str, default='')

    def __init__(self, store):
        super().__init__()

        self.set_name('note-list-view')

        self.build_ui()
        self.connect_events()

        store.subscribe(self.set_state)
        self.connect_store(store)
        self.set_state(store.state)

    def connect_events(self):
        self.connect('notify::notes', lambda source, param: self.on_notify_notes())
        self.connect('notify::current-note', lambda source, param: self.on_notify_current_note())

    def on_notify_notes(self):
        self.list_model().update(self.get_property('notes'))
        self.scroll_current_cell_into_view()

    def on_notify_current_note(self):
        self.scroll_current_cell_into_view()

    def set_state(self, state):
        if self.get_property('notes') != state.get('notes'):
            self.set_property('notes', state.get('notes'))

        if self.get_property('current-note') != state.get('current_note_id'):
            self.set_property('current-note', state.get('current_note_id'))

    def connect_store(self, store):
        self.tree_view.get_selection().connect(
            'changed',
            lambda selection: store.dispatch(
                select_note(self.selected_note_id(selection)))
        )

    def selected_note_id(self, selection):
        model, treeiter = selection.get_selected()
        return model[treeiter][0]

    def list_model(self):
        return self.tree_view.get_model()

    def build_ui(self):
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

    def select_first(self):
        first_iter = self.list_model().get_iter_first()
        self.tree_view.get_selection().select_iter(first_iter)

    def select_next(self):
        selection = self.tree_view.get_selection()
        model, current_iter = selection.get_selected()
        next_iter = model.iter_next(current_iter)
        if next_iter is not None:
            selection.select_iter(next_iter)

    def select_previous(self):
        selection = self.tree_view.get_selection()
        model, current_iter = selection.get_selected()
        prev_iter = model.iter_previous(current_iter)
        if prev_iter is not None:
            selection.select_iter(prev_iter)

    def scroll_current_cell_into_view(self):
        note_id = self.get_property('current-note')

        if note_id:
            self.tree_view.scroll_to_cell(self.list_model().get_tree_path_by_note(note_id))
