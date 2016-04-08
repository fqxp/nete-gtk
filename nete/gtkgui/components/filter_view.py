from gi.repository import Gtk, GObject
from nete.gtkgui.state.actions import change_filter_term


class FilterView(Gtk.Box):

    filter_term = GObject.property(type=str, default='')

    def __init__(self, store):
        super().__init__(spacing=4)

        self.build_ui(store)
        self.connect_events()

        store.subscribe(self.set_state)

    def set_state(self, state):
        if state['filter_term'] != self.get_property('filter_term'):
            self.set_property('filter_term', state['filter_term'])

    def connect_store(self, store):
        self.filter_term_entry.connect(
            'notify::text',
            lambda source, param: store.dispatch(change_filter_term(self.filter_term_entry.get_text())))

    def build_ui(self, store):
        self.filter_term_entry = Gtk.Entry()
        self.add(self.filter_term_entry)

    def connect_events(self):
        self.connect('notify::filter_term', lambda source, param: self.on_notify_filter_term)

    def on_notify_filter_term(self):
        if self.get_property('filter_term') != self.filter_term_entry.get_text():
            self.filter_term_entry.set_text(self.get_property('filter_term'))
