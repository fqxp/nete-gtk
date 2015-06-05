from nete.models.nete_uri import NeteUri, MalformedNeteUri
import unittest


class NeteUriTest(unittest.TestCase):

    def test_correct_uri_is_parsed(self):
        nete_uri = NeteUri('nete:foo')
        self.assertEqual(nete_uri.context, 'foo')

    def test_incorrect_uri_raises_exception(self):
        with self.assertRaises(MalformedNeteUri):
            NeteUri('http://example.org')

    def test_unicode_representation(self):
        nete_uri = NeteUri('nete:foo')
        self.assertEqual(unicode(nete_uri), 'nete:foo')

