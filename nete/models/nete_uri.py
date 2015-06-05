import re


class MalformedNeteUri(Exception):
    def __init__(self, uri):
        super(MalformedNeteUri, self).__init__('%s is not a nete URI' % uri)
        self.uri = uri


class NeteUri(object):

    NETE_URI_RE = re.compile(r'^nete:(?P<context>.*)$')

    def __init__(self, uri):
        self._interpret_uri(uri)

    @property
    def context(self):
        return self._context

    def _interpret_uri(self, uri):
        match = self.NETE_URI_RE.match(uri)
        if match is None:
            raise MalformedNeteUri(uri)

        self._context = match.group('context')

    def __unicode__(self):
        return 'nete:%(context)s' % {
            'context': self.context,
        }
