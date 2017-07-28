from gi.repository import Gtk, GObject
from nete.gtkgui.actions import change_filter_term, set_filter_term_entry_focus
from fluous.gobject import connect


class FilterView(Gtk.Box):

    has_focus = GObject.property(type=bool, default=False)
    filter_term = GObject.property(type=str, default='')

    def __init__(self):
        super().__init__()
        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.filter_term_entry = Gtk.Entry()
        self.pack_start(self.filter_term_entry, True, True, 2)

    def _connect_events(self):
        self.bind_property('filter-term', self.filter_term_entry, 'text', GObject.BindingFlags.BIDIRECTIONAL)
        self.bind_property('has-focus', self.filter_term_entry, 'has-focus', GObject.BindingFlags.BIDIRECTIONAL)


def map_state_to_props(state):
    return (
        ('filter-term', state['ui_state']['filter_term']),
        ('has-focus', state['ui_state']['filter_term_entry_focus']),
    )


def map_dispatch_to_props(dispatch):
    return {
        'notify::filter-term': lambda source, param:
            dispatch(change_filter_term(source.get_property('filter-term'))),
        'notify::has-focus': lambda source, param:
            dispatch(set_filter_term_entry_focus(source.get_property('has_focus'))),
    }


ConnectedFilterView = connect(FilterView, map_state_to_props, map_dispatch_to_props)
