from gi.repository import GObject


class Note(GObject.Object):

    __gsignals__ = {
        'changed': (GObject.SIGNAL_RUN_FIRST, None, (GObject.Object, )),
    }

    def __init__(self, note):
        super().__init__()
        self.note = note

    def save(self):
        self.note.save()

    @GObject.property
    def title(self):
        return self.note.title

    @title.setter
    def title(self, title):
        is_changed = (self.note.title != title)
        self.note.title = title
        if is_changed:
            self.emit('changed', self)

    @GObject.property
    def text(self):
        return self.note.text

    @text.setter
    def text(self, text):
        is_changed = (self.note.text != text)
        self.note.text = text
        if is_changed:
            self.emit('changed', self)

