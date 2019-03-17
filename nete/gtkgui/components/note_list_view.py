from gi.repository import Gtk, GObject, Pango


class NoteListView(Gtk.TreeView):

    notes = GObject.property(type=GObject.TYPE_PYOBJECT)
    current_note_title = GObject.property(type=str, default='')
    preselected_note_title = GObject.property(type=str, default='')

    __gsignals__ = {
        'preselect-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION,
                           None,
                           (str,)),
        'select-note': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION,
                        None,
                        (str,)),
    }

    def __init__(self, **kwargs):
        super().__init__(
            model=NoteListModel(),
            headers_visible=False,
            can_focus=False,
            **kwargs)

        self._build_ui()
        self._connect_events()
        self.set_activate_on_single_click(True)

        self.get_model().update(self.get_property('notes'), self.get_property('current_note_title'))

    def _build_ui(self):
        title_renderer = Gtk.CellRendererText(
            ellipsize=Pango.EllipsizeMode.END
        )
        column = Gtk.TreeViewColumn(
            'title',
            title_renderer,
            text=self.get_model().COLUMN_NOTE_TITLE)
        column.add_attribute(title_renderer, 'background', self.get_model().COLUMN_NOTE_BGCOLOR)
        self.append_column(column)

    def _connect_events(self):
        self.connect('notify::notes', self.on_notify_notes)
        self.connect('notify::current-note-title', self.on_notify_current_note_title)
        self.connect('row_activated', self.on_row_activated)
        self._changed_selection_handler = self.get_selection().connect(
            'changed',
            self.on_changed_selection)
        self._notify_preselected_note_title_handler = self.connect(
            'notify::preselected-note-title',
            self.on_notify_preselected_note_title)

    def on_notify_notes(self, source, param):
        self.get_model().update(self.get_property('notes'), self.get_property('current_note_title'))
        self.update_selection()

    def on_notify_current_note_title(self, source, param):
        self.get_model().update(self.get_property('notes'), self.get_property('current_note_title'))

    def on_row_activated(self, source, path, column):
        index = path.get_indices()[0]
        note_title = self.get_property('notes')[index]['title']
        self.emit('select-note', note_title)

    def on_changed_selection(self, selection):
        model, treeiter = self.get_selection().get_selected()

        note_title = (
            model[treeiter][NoteListModel.COLUMN_NOTE_TITLE]
            if treeiter is not None
            else None
        )

        with self.handler_block(self._notify_preselected_note_title_handler):
            self.emit('preselect-note', note_title)

    def on_notify_preselected_note_title(self, source, param):
        self.update_selection()

    def update_selection(self):
        if self.get_property('preselected_note_title') is None:
            self.get_selection().unselect_all()
            return

        treeiter = self.get_model().get_treeiter_by_note_title(self.get_property('preselected_note_title'))

        if treeiter is None:
            return

        self.get_selection().select_iter(treeiter)

        self.scroll_note_into_view(treeiter)

    def preselected_note(self):
        model, treeiter = self.get_selection().get_selected()

        if treeiter is None:
            return None

        return model[treeiter][model.COLUMN_NOTE_TITLE]

    def scroll_note_into_view(self, treeiter):
        tree_path = self.get_model().get_path(treeiter)
        self.scroll_to_cell(tree_path)


class NoteListModel(Gtk.ListStore):

    COLUMN_NOTE_TITLE = 0
    COLUMN_NOTE_BGCOLOR = 1

    def __init__(self):
        super().__init__(str, str)

    def update(self, note_list, current_note_title):
        visible_note_list = [note
                     for note in note_list
                     if note['visible']]
        notes_by_title = {note['title']: note
                          for note in visible_note_list}

        self._delete_rows(notes_by_title)
        self._update_rows(notes_by_title, current_note_title)
        self._append_rows(visible_note_list, current_note_title)
        self._sync_order(visible_note_list)

    def _delete_rows(self, notes_by_title):
        rows_to_delete = [
            row
            for row in self
            if row[self.COLUMN_NOTE_TITLE] not in notes_by_title]

        for row in rows_to_delete:
            self.remove(row.iter)

    def _update_rows(self, notes_by_title, current_note_title):
        for row in self:
            note = notes_by_title[row[self.COLUMN_NOTE_TITLE]]
            row[self.COLUMN_NOTE_TITLE] = note['title']
            row[self.COLUMN_NOTE_BGCOLOR] = self._background_color(note['title'], current_note_title)

    def _append_rows(self, note_list, current_note_title):
        row_titles = [row[self.COLUMN_NOTE_TITLE] for row in self]
        rows_to_append = [
            [
                note['title'],
                self._background_color(note['title'], current_note_title)
            ]
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

    def _background_color(self, note_title, current_note_title):
        return '#aaaaaa' if note_title == current_note_title else '#ffffff'
