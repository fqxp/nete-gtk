from gi.repository import Gtk, GObject
from nete.gtkgui.actions import change_filter_term, set_filter_term_entry_focus
from fluous.gobject import connect


class FilterView(Gtk.Box):

    has_focus = GObject.property(type=bool, default=False)
    filter_term = GObject.property(type=str, default='')

    __gsignals__ = {
        'filter-term-entry-focus-changed': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (bool, )),
        'filter-term-changed': (GObject.SIGNAL_RUN_FIRST|GObject.SIGNAL_ACTION, None, (str, )),
    }

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.filter_term_entry = Gtk.Entry()
        self.pack_start(self.filter_term_entry, True, True, 2)

    def _connect_events(self):
        self.bind_property('filter-term', self.filter_term_entry, 'text', GObject.BindingFlags.BIDIRECTIONAL)
        self.connect('notify::filter-term', lambda source, param: self.on_notify_filter_term())

        self.bind_property('has-focus', self.filter_term_entry, 'has-focus', GObject.BindingFlags.BIDIRECTIONAL)
        self.connect('notify::has-focus', lambda source, param: self.on_notify_has_focus())

    def on_notify_filter_term(self):
        self.emit('filter-term-changed', self.filter_term)

    def on_notify_has_focus(self):
        self.emit('filter-term-entry-focus-changed', self.has_focus)


def map_state_to_props(state):
    return (
        ('filter-term', state['ui_state']['filter_term']),
        ('has-focus', state['ui_state']['filter_term_entry_focus']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'filter-term-changed': lambda filter_term:
            dispatch(change_filter_term(filter_term)),
        'filter-term-entry-focus-changed': lambda has_focus:
            dispatch(set_filter_term_entry_focus(has_focus)),
    }


ConnectedFilterView = connect(FilterView, map_state_to_props, map_dispatch_to_props)
