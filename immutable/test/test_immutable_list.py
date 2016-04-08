from immutable import ImmutableDict, ImmutableList
from nose2.tools import such
from collections.abc import Iterable


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
