from gi.repository import Gtk, GObject
from .models.note import Note


class NoteListView(Gtk.Grid):

    __gsignals__ = {
        'selection-changed': (GObject.SIGNAL_RUN_FIRST, None, (Note, )),
    }

    def __init__(self, model):
        super().__init__()

        self.set_name('note-list-view')
        self.build_ui(model)

    @GObject.property
    def model(self):
        return self.tree_view.get_model()

    def build_ui(self, model):
        self.scrollable_treelist = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True,
            can_focus=False)
        self.attach(self.scrollable_treelist, 0, 0, 1, 1)

        self.tree_view = Gtk.TreeView(model, headers_visible=False, can_focus=False)
        title_renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('title', title_renderer, text=1)
        self.tree_view.append_column(column)

        self.scrollable_treelist.add(self.tree_view)

        self.tree_view.get_selection().connect('changed', self.on_selection_changed)

    def select_first(self):
        self.tree_view.get_selection().select_iter(self.model.get_iter_first())

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

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        self.tree_view.scroll_to_cell(model.get_path(treeiter))

        note = model[treeiter][0]
        self.emit('selection-changed', note)

