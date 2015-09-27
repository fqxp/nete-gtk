from gi.repository import GObject


class Note(GObject.Object):

    def __init__(self, note):
        super().__init__()
        self.note = note

    @GObject.property
    def title(self):
        return self.note.title

    @GObject.property
    def text(self):
        return self.note.text

