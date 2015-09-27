from gi.repository import Gtk, GObject


class NoteTextView(Gtk.Grid):

    def __init__(self):
        super().__init__()

        self.build_ui()

    @GObject.property
    def text(self):
        return self.text_view.get_buffer().get_text()

    @text.setter
    def text(self, text):
        self.text_view.get_buffer().set_text(text)

    def build_ui(self):
        scrollable_text_view = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True)

        self.text_view = Gtk.TextView()
        scrollable_text_view.add(self.text_view)

        self.attach(scrollable_text_view, 0, 0, 1, 1)
