from gi.repository import GObject
from fluous.gobject import connect
from nete.services.ui_state_storage import load_ui_state, save_ui_state


def on_ui_state_changed(ui_state, dispatch):
    save_ui_state(ui_state)
