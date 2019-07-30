from gi.repository import Gdk, Gtk, GObject


class FilterView(Gtk.Bin):

    filter_term = GObject.Property(type=str, default='')

    __gsignals__ = {
        'filter-term-changed':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, (str,)),
        'keyboard-down':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'keyboard-up':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'select-preselected-note':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
        'reset':
            (GObject.SignalFlags.RUN_FIRST | GObject.SignalFlags.ACTION, None, tuple()),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.filter_term_entry = Gtk.Entry(
            name='filter_term_entry',
            text=self.filter_term,
            placeholder_text='Filter notes (Ctrl-F) ...',
            secondary_icon_name='edit-clear-symbolic',
            secondary_icon_activatable=True,
        )
        self.add(self.filter_term_entry)

    def _connect_events(self):
        self.bind_property('filter-term',
                           self.filter_term_entry,
                           'text',
                           GObject.BindingFlags.DEFAULT)

        self.filter_term_entry.connect(
            'activate',
            lambda source: (self.emit('select-preselected-note')))
        self.filter_term_entry.connect(
            'changed',
            lambda source: (
                self.emit('filter-term-changed', source.get_property('text'))))
        self.filter_term_entry.connect('key-press-event', self._on_key_press_event)
        self.filter_term_entry.connect('key-release-event', self._on_key_release_event)
        self.filter_term_entry.connect('icon-release', self._on_icon_release)

    def _on_key_press_event(self, source, event_key):
        if event_key.keyval == Gdk.KEY_Down:
            self.emit('keyboard-down')
            return True
        elif event_key.keyval == Gdk.KEY_Up:
            self.emit('keyboard-up')
            return True
        else:
            return False

    def _on_key_release_event(self, source, event_key):
        if event_key.keyval == Gdk.KEY_Escape:
            self.emit('reset')
            return True
        else:
            return False

    def _on_icon_release(self, entry, icon_pos, event):
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.filter_term_entry.props.text = ''
