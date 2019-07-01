from gi.repository import Gdk, Gtk, GObject


class FilterView(Gtk.Bin):

    has_focus = GObject.property(type=bool, default=False)
    filter_term = GObject.property(type=str, default='')

    __gsignals__ = {
        'filter-term-changed':
            (GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, None, (str,)),
        'focused':
            (GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, None, tuple()),
        'keyboard-down':
            (GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, None, tuple()),
        'keyboard-up':
            (GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, None, tuple()),
        'select-preselected-note':
            (GObject.SIGNAL_RUN_FIRST | GObject.SIGNAL_ACTION, None, tuple()),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.filter_term_entry = Gtk.Entry(text=self.filter_term)
        self.add(self.filter_term_entry)

    def _connect_events(self):
        self.bind_property('filter-term',
                           self.filter_term_entry,
                           'text',
                           GObject.BindingFlags.DEFAULT)
        self.bind_property('has-focus',
                           self.filter_term_entry,
                           'has-focus',
                           GObject.BindingFlags.DEFAULT)

        self.filter_term_entry.connect(
            'activate',
            lambda source: (self.emit('select-preselected-note')))
        self.filter_term_entry.connect(
            'changed',
            lambda source: (
                self.emit('filter-term-changed', source.get_property('text'))))
        self.filter_term_entry.connect(
            'focus-in-event',
            lambda source, direction: (self.emit('focused')))
        self.filter_term_entry.connect(
            'key-press-event',
            self.on_key_press_event)

    def on_key_press_event(self, source, event_key):
        if event_key.keyval == Gdk.KEY_Down:
            self.emit('keyboard-down')
            return True
        elif event_key.keyval == Gdk.KEY_Up:
            self.emit('keyboard-up')
            return True
        else:
            return False
