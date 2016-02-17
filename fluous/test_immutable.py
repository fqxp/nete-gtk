from fluous.immutable import ImmutableDict, ImmutableList
import unittest
from nose2.tools import such
from collections.abc import Iterable


with such.A('ImmutableDict') as it:

    with it.having('__init__'):
        @it.should('make nested values immutable')
        def test():
            d = ImmutableDict({
                'map': {'b': 1},
                'list': [1, 2, 3],
                'set': set((4, 5, 6)),
            })

            it.assertIsInstance(d['map'], ImmutableDict)
            it.assertIsInstance(d['list'], ImmutableList)
            it.assertIsInstance(d['set'], frozenset)

        @it.should('assign copy of `initial` argument to data attribute')
        def test():
            initial = {'a': 1}
            d = ImmutableDict(initial)
            it.assertEqual(d.data, initial)
            it.assertIsNot(d.data, initial)

        @it.should('assign data from other ImmutableDict when given as initial parameter')
        def test():
            initial = ImmutableDict({'a': 1})
            d = ImmutableDict(initial)
            it.assertIs(d.data, initial.data)

        @it.should('raise ValueError if initial argument is not a mapping')
        def test():
            it.assertRaises(ValueError, ImmutableDict, 'NOT A MAPPING')

        @it.should('raise ValueError if initial argument contains a mutable value')
        def test():
            initial = {'a': object()}
            it.assertRaises(ValueError, ImmutableDict, initial)

    with it.having('set'):
        @it.should('return new immutable dict with changed value')
        def test():
            old = ImmutableDict({'a': 1})
            new = old.set('a', 2)

            it.assertEqual(old['a'], 1)
            it.assertEqual(new['a'], 2)

        @it.should('return same instance if value is unchanged')
        def test():
            old = ImmutableDict({'a': 1})
            new = old.set('a', 1)

            it.assertIs(new, old)

    with it.having('update'):
        @it.should('return new immutable dict with updated values')
        def test():
            old = ImmutableDict({'a': 1, 'b': 2})
            new = old.update({'a': 100, 'b': 200})

            it.assertEqual(old['a'], 1)
            it.assertEqual(old['b'], 2)
            it.assertEqual(new['a'], 100)
            it.assertEqual(new['b'], 200)

        @it.should('return same instance if values are unchanged')
        def test():
            old = ImmutableDict({'a': 1, 'b': 2})
            new = old.update({'a': 1})

            it.assertIs(new, old)

    with it.having('del'):
        @it.should('return new immutable dict with key removed')
        def test():
            old = ImmutableDict({'a': 1, 'b': 2})
            new = old.delete('a')

            it.assertIn('a', old)
            it.assertNotIn('a', new)

        @it.should('raise KeyError if key is not in map')
        def test():
            old = ImmutableDict({'a': 1, 'b': 2})

            it.assertRaises(KeyError, old.delete, 'x')

    with it.having('__getitem__'):
        @it.should('return value associated with key')
        def test():
            d = ImmutableDict({'a': 1})
            it.assertEqual(d['a'], 1)

        @it.should('raise KeyError if key is not in map')
        def test():
            d = ImmutableDict({'a': 1})
            it.assertRaises(KeyError, d.__getitem__, 'x')

    with it.having('__iter__'):
        @it.should('return an iterator over all keys')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            iterator = iter(d)
            it.assertIsInstance(iterator, Iterable)
            it.assertEqual(['a', 'b'], sorted(iterator))

    with it.having('__len__'):
        @it.should('return the number of keys')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual(len(d), 2)

    with it.having('__contains__'):
        @it.should('returns whether mapping contains key')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertTrue('a' in d)
            it.assertFalse('x' in d)

    with it.having('keys'):
        @it.should('return all keys')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual(['a', 'b'], sorted(d.keys()))

    with it.having('items'):
        @it.should('return (key, value) tuples')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual([('a', 1), ('b', 2)], sorted(d.items()))

    with it.having('values'):
        @it.should('return all values')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual([1, 2], sorted(d.values()))

    with it.having('get'):
        @it.should('return value associated to key')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual(1, d.get('a'))

        @it.should('return default value if mapping does not have key')
        def test():
            d = ImmutableDict({'a': 1, 'b': 2})
            it.assertEqual(666, d.get('x', 666))

    with it.having('__eq__'):
        @it.should('return True if mapping has same keys and values as other mapping')
        def test():
            d1 = ImmutableDict({'a': 1, 'b': 2})
            d2 = ImmutableDict({'a': 1, 'b': 2})
            d3 = ImmutableDict({'x': 1})

            it.assertTrue(d1 == d2)
            it.assertFalse(d2 == d3)

        @it.should('return False if other mapping is not an ImmutableDict')
        def test():
            d1 = ImmutableDict({'a': 1, 'b': 2})
            d2 = {'a': 1, 'b': 2}

            it.assertFalse(d1 == d2)

    with it.having('__hash__'):
        @it.should('return same hash value iff mapping has same keys and values as other mapping')
        def test():
            d1 = ImmutableDict({'a': 1, 'b': {'c': 2}})
            d2 = ImmutableDict({'a': 1, 'b': {'c': 2}})
            d3 = ImmutableDict({'a': 1, 'b': {'c': 42}})

            it.assertEqual(hash(d1), hash(d2))
            it.assertNotEqual(hash(d2), hash(d3))

    it.createTests(globals())


with such.A('ImmutableList') as it:

    with it.having('__init__'):
        @it.should('make nested values immutable')
        def test():
            l = ImmutableList([
                {'b': 1},
                [1, 2, 3],
                set((4, 5, 6)),
            ])

            it.assertIsInstance(l[0], ImmutableDict)
            it.assertIsInstance(l[1], ImmutableList)
            it.assertIsInstance(l[2], frozenset)

        @it.should('assign copy of `initial` argument to data attribute')
        def test():
            initial = [1, 2, 3]
            l = ImmutableList(initial)
            it.assertEqual(l.data, initial)
            it.assertIsNot(l.data, initial)

        @it.should('assign data from other ImmutableList when given as initial parameter')
        def test():
            initial = ImmutableList([1, 2, 'a'])
            l = ImmutableList(initial)
            it.assertIs(l.data, initial.data)

        @it.should('raise ValueError if `initial` argument is not a sequence')
        def test():
            it.assertRaises(ValueError, ImmutableList, 42)

        @it.should('raise ValueError if `initial` argument contains a mutable value')
        def test():
            initial = [object()]
            it.assertRaises(ValueError, ImmutableList, initial)

    with it.having('__getitem__'):
        @it.should('return value at index')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(l[1], 'b')

    with it.having('__len__'):
        @it.should('return length of sequence')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(len(l), 3)

    with it.having('__contains__'):
        @it.should('return True iff sequence contains value')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertTrue('a' in l)
            it.assertFalse('x' in l)

    with it.having('__iter__'):
        @it.should('return an iterator over all values')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            iterator = iter(l)
            it.assertIsInstance(iterator, Iterable)
            it.assertEqual(['a', 'b', 'c'], list(iterator))

    with it.having('__reverse__'):
        @it.should('return values in reverse')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(list(reversed(l)), ['c', 'b', 'a'])

    with it.having('__add__'):
        @it.should('return a new ImmutableList with values from other sequence appended to the end')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(l + ['d', 'e'], ImmutableList(['a', 'b', 'c', 'd', 'e']))

    with it.having('index'):
        @it.should('return index of value')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(l.index('b'), 1)

    with it.having('count'):
        @it.should('return how many times value is contained')
        def test():
            l = ImmutableList(['a', 'c', 'a', 'b'])
            it.assertEqual(l.count('a'), 2)

    with it.having('set'):
        @it.should('return new immutable dict with changed value')
        def test():
            old = ImmutableList(['a', 'b', 'c'])
            new = old.set(1, 'x')

            it.assertEqual(old[1], 'b')
            it.assertEqual(new[1], 'x')

        @it.should('return same instance if value is unchanged')
        def test():
            old = ImmutableList(['a', 'b', 'c'])
            new = old.set(1, 'b')

            it.assertIs(new, old)

    with it.having('append'):
        @it.should('return a new ImmutableList with value appended to the end')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(l.append('d'), ImmutableList(['a', 'b', 'c', 'd']))

    with it.having('extend'):
        @it.should('return a new ImmutableList with values from other sequence appended to the end')
        def test():
            l = ImmutableList(['a', 'b', 'c'])
            it.assertEqual(l.extend(['d', 'e']), ImmutableList(['a', 'b', 'c', 'd', 'e']))

    with it.having('remove'):
        @it.should('return new immutable list with first occurence of value removed')
        def test():
            old = ImmutableList(['a', 'c', 'a', 'b'])
            new = old.remove('a')

            it.assertEqual(list(new), ['c', 'a', 'b'])

        @it.should('raise ValueError if value is not in sequence')
        def test():
            l = ImmutableList(['a', 'b', 'c'])

            it.assertRaises(ValueError, l.remove, 'x')

    with it.having('__eq__'):
        @it.should('return True if sequence has same elements as other sequence')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ImmutableList(['a', 'b', 'c'])
            l3 = ImmutableList(['x'])

            it.assertTrue(l1 == l2)
            it.assertFalse(l1 == l3)

        @it.should('return False if other argument is not an immutable list')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ['a', 'b', 'c']

            it.assertFalse(l1 == l2)

    with it.having('__ne__'):
        @it.should('return False if sequence has different elements than other sequence')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ImmutableList(['a', 'b', 'c'])
            l3 = ImmutableList(['x'])

            it.assertTrue(l1 == l2)
            it.assertFalse(l1 == l3)

        @it.should('return True if other argument is not an immutable list')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ['x']

            it.assertFalse(l1 == l2)

    with it.having('__eq__'):
        @it.should('return True if sequence has same elements as other sequence')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ImmutableList(['a', 'b', 'c'])
            l3 = ImmutableList(['x'])

            it.assertFalse(l1 != l2)
            it.assertTrue(l1 != l3)

    with it.having('__hash__'):
        @it.should('return same hash value iff sequence has same values as other mapping')
        def test():
            l1 = ImmutableList(['a', 'b', 'c'])
            l2 = ImmutableList(['a', 'b', 'c'])
            l3 = ImmutableList(['x'])

            it.assertEqual(hash(l1), hash(l2))
            it.assertNotEqual(hash(l2), hash(l3))

    it.createTests(globals())
