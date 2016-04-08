from nose2.tools import such
from immutable import get_by_path, set_by_path, ImmutableDict


with such.A('get_by_path') as it:

    @it.should('return the value for key for a path with one element')
    def test():
        d = {'a': 42}
        result = get_by_path(d, ('a',))
        it.assertEqual(result, 42)

        d = [1, 2, 3]
        result = get_by_path(d, (1, ))
        it.assertEqual(result, 2)

    @it.should('return the value for key for a path with two elements')
    def test():
        d = {'a': [1, 2, 3]}
        result = get_by_path(d, ('a', 1))
        it.assertEqual(result, 2)

        d = [1, {'a': 42}, 2]
        result = get_by_path(d, (1, 'a'))
        it.assertEqual(result, 42)

    @it.should('raise KeyError for an empty key')
    def test():
        d = {'a': 42}
        it.assertRaises(KeyError, get_by_path, d, tuple())

    it.createTests(globals())


with such.A('set_by_path') as it:

    @it.should('return ImmutableDict with path value set to new value')
    def test():
        d = ImmutableDict({'a': 42})
        result = set_by_path(d, ('a'), 23)
        it.assertEqual(result, ImmutableDict({'a': 23}))

        d = ImmutableDict({'a': {'b': {'c': ['foo', 'bar', 'baz']}}})
        result = set_by_path(d, ('a', 'b', 'c', 1), 23)
        it.assertEqual(result, ImmutableDict({'a': {'b': {'c': ['foo', 23, 'baz']}}}))

    @it.should('return same instance if value is unchanged')
    def test():
        d = ImmutableDict({'a': {'b': {'c': ['foo', 'bar', 'baz']}}})
        result = set_by_path(d, ('a', 'b', 'c', 1), 'bar')
        it.assertIs(result, d)

    @it.should('raise KeyError for an empty key')
    def test():
        d = {'a': 42}
        it.assertRaises(KeyError, set_by_path, d, tuple(), 23)

    it.createTests(globals())
