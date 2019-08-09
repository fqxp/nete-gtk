import xml.sax
from gi.repository import GLib, Gtk, GObject
import gi.repository


class UiDefinition:

    @classmethod
    def load(cls, filename):
        ui_def = UiDefinition()
        state = 'root'

        self.reader = xml.sax.parse(filename)

    def build():
        pass


class UiContentHandler(xml.sax.ContentHandler):

    def __init__(self):
        super().__init__()
        self.state = None
        self.root = None
        self.stack = []

    def startElement(self, name, attrs):
        attrs = dict(items(attrs))

        if self.state is None:
            self._root_element(name, attrs)

        elif name == 'signal':
            _signal(attrs)

    def _root_element(self, name, attrs):
        namespace = attrs.getValue('namespace') or 'Gtk'
        module = getattr(gi.repository, namespace)
        widget = getattr(module, name)
        self.root = widget(attrs)
        self.root.__gsignals__ = {}

    def _signal(self, attrs):
        assert len(self.stack) == 0

        self.root.__gsignals__[attrs['name']] = (
            self._signalflag_by_name(flag)
            for flag in attrs['flags'].split():
        )

    def _signalflag_by_name(self, name):
        if name == 'RUN_FIRST':
            return GObject.SignalFlags.RUN_FIRST
        else:
            raise
