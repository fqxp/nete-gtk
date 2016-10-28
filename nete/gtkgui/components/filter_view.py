from gi.repository import Gtk, GObject
from nete.gtkgui.actions import (
    change_filter_term, set_filter_term_entry_focus)
from flurx import create_component


def create_filter_view(store):
    return create_component(FilterView, store, map_state_to_props)


def map_state_to_props(state):
    return (
        ('filter-term', state['ui_state']['filter_term']),
        ('has-focus', state['ui_state']['filter_term_entry_focus']),
    )


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

        self.connect('notify::filter-term', lambda *args: change_filter_term(self.filter_term))
        self.connect('notify::has-focus', lambda *args: set_filter_term_entry_focus(self.has_focus))
