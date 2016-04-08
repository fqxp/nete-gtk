from gi.repository import GObject
from fluous.gobject import connect
from .ui_state_storage import load_ui_state, save_ui_state


def map_state_to_props(state):
    return (
        ('ui_state', state['ui_state']),
    )


class UiStatePersistence(GObject.GObject):

    ui_state = GObject.property(type=GObject.TYPE_PYOBJECT)

    def __init__(self):
        super().__init__()
        self._connect_events()

    def _connect_events(self):
        self.connect(
            'notify',
            lambda source, param: self._on_notify())

    def _on_notify(self):
        save_ui_state(self.get_property('ui_state'))


ConnectedUiStatePersistence = connect(UiStatePersistence, map_state_to_props)
