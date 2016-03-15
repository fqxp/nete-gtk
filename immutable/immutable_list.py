import collections.abc
import types
from .functions import make_immutable


class ImmutableList(collections.abc.Sequence):

    def __init__(self, initial=[]):
        if isinstance(initial, ImmutableList):
            self.data = initial.data
        elif (isinstance(initial, collections.abc.MutableSequence) or
              isinstance(initial, types.GeneratorType)):
            self.data = self._copy(initial)
        else:
            raise ValueError('Argument `initial` must be sequence')

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        return iter(self.data)

    def __reversed__(self):
        return reversed(self.data)

    def __add__(self, other):
        return ImmutableList(self.data + other)

    def index(self, value):
        return self.data.index(value)

    def count(self, value):
        return self.data.count(value)

    def set(self, index, value):
        if len(self.data) > index and self.data[index] == value:
            return self

        new = ImmutableList(self.data)
        new.data[index] = make_immutable(value)
        return new

    def set_by_path(self, path, value):
        return set_by_path(self, path, value)

    def append(self, value):
        return ImmutableList(self.data + [value])

    def extend(self, data):
        return self + data

    def remove(self, value):
        new = ImmutableList(self.data)
        new.data.remove(value)
        return new

    def __eq__(self, other):
        return isinstance(other, ImmutableList) and hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return sum(map(hash, self.data))

    def _copy(self, data):
        return list(map(make_immutable, data))
