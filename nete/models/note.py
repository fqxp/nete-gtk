class Note(object):

    def __init__(self):
        self._id = None
        self._title = ''
        self._text = ''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    def __unicode__(self):
        return '<Note id=%r title=%s text=%s...>' % (
            self.id, self.title, self.text[:30])
