from fluous.gobject import connect
from gi.repository import Gtk, GLib, GObject


class InfoBar(Gtk.InfoBar):

    REVEAL_TIMEOUT = 5

    info_message = GObject.Property(type=str)

    def __init__(self, **kwargs):
        super().__init__(
            message_type=Gtk.MessageType.WARNING,
            revealed=False,
            show_close_button=True,
        )

        self._info_bar_event_source_id = None

        self._build_ui()
        self._connect_events()

    def _build_ui(self):
        self.label = Gtk.Label()
        self.get_content_area().add(self.label)

    def _connect_events(self):
        self.bind_property(
            'info-message',
            self.label,
            'label',
            GObject.BindingFlags.DEFAULT)

        self.connect('notify::info-message', self._on_notify_info_message)
        self.connect('response', self._on_infobar_response)

    def _on_notify_info_message(self, source, params):
        if self.props.info_message:
            self.props.revealed = True
            self._add_infobar_timeout()
        else:
            self.props.revealed = False
            self._remove_infobar_timeout()

    def _on_infobar_response(self, info_bar, response_id):
        if response_id == Gtk.ResponseType.CLOSE:
            self.props.revealed = False

    def _remove_infobar_timeout(self):
        if self._info_bar_event_source_id is not None:
            GLib.Source.remove(self._info_bar_event_source_id)
            self._info_bar_event_source_id = None

    def _add_infobar_timeout(self):
        self._remove_infobar_timeout()
        self._info_bar_event_source_id = GLib.timeout_add_seconds(
            priority=GLib.PRIORITY_DEFAULT,
            interval=self.REVEAL_TIMEOUT,
            function=self._on_infobar_timeout)

    def _on_infobar_timeout(self):
        self.props.revealed = False
        self._info_bar_event_source_id = None
        return False


def map_state_to_props(state):
    return (
        ('info-message', state['ui']['info_message']),
    )


ConnectedInfoBar = connect(InfoBar, map_state_to_props)
