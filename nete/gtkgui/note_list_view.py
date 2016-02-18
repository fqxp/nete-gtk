from gi.repository import Gdk, Gtk, GObject, Pango
from .models.note import Note
from nete.gtkgui.state.actions import select_note


class NoteListModel(Gtk.ListStore):
    nete_uri = GObject.property(type=str)

    def __init__(self):
        super().__init__(str, str)

    def update_from_list(self, note_data):
        self.clear()
        for note in note_data:
            self.append([note['id'], note['title']])

    # def on_note_changed(self, note):
        # tree_iter = self.get_treeiter_for_note(note)
        # self[tree_iter] = (note, note.title)

    def get_treeiter_for_note(self, note_id):
        tree_iter = self.get_iter_first()

        while tree_iter is not None:
            if self[tree_iter][0] == note_id:
                return tree_iter
            tree_iter = self.iter_next(tree_iter)

        raise Exception('note not found')

    def get_tree_path_for_note(self, note_id):
        treeiter = self.get_treeiter_for_note(note_id)
        return self.get_path(treeiter)


class NoteListView(Gtk.Grid):

    notes = GObject.property(type=GObject.TYPE_PYOBJECT)
    current_note = GObject.property(type=str, default='')

    def __init__(self, store):
        super().__init__()

        self._selected_iter = None

        self.set_name('note-list-view')

        self.build_ui()
        self.connect_events()

        store.subscribe(self.set_state)
        self.connect_store(store)
        self.set_state(store.state)

    def connect_events(self):
        self.connect('notify::notes', self.on_notify_notes)
        self.connect('notify::current-note', self.on_notify_current_note)

    def on_notify_notes(self, obj, gparamstring):
        self.list_model().update_from_list(self.get_property('notes'))

    def on_notify_current_note(self, source, param_name):
        selected_note_id = self.get_property('current-note')

        self.tree_view.scroll_to_cell(self.list_model().get_tree_path_for_note(selected_note_id))

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
        model, tree_iter = selection.get_selected()
        return model[tree_iter][0]

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
        model = self.list_model()
        first_iter = model.get_iter_first()
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
