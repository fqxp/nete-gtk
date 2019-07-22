import logging

from gi.repository import GObject, Gtk

logger = logging.getLogger(__name__)


class FocusManager(GObject.Object):

    focus = GObject.Property(type=str)

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        self.connect('notify::focus', self._on_notify_focus)

    def _on_notify_focus(self, source, params):
        if self.props.focus is None:
            self.window.set_focus(None)
        else:
            widget = self._find_widget_by_name(self.props.focus)
            if widget is None:
                logger.warn(
                    '_on_notify_focus: widget {} not found!'.format(widget))
                return
            self.window.set_focus(widget)

    def _find_widget_by_name(self, name):
        for (widget, _) in self._walk_tree():
            if widget.get_property('name') == name:
                return widget

    def _walk_tree(self, widget=None, level=0):
        if widget is None:
            widget = self.window

        for child_widget in widget.get_children():
            yield (child_widget, level)

            if isinstance(child_widget, Gtk.Container):
                yield from self._walk_tree(child_widget, level + 1)
