import copy
import collections
import collections.abc


def make_immutable(value):
    if isinstance(value, collections.MutableMapping):
        return ImmutableDict(value)
    elif isinstance(value, collections.MutableSequence):
        return ImmutableList(value)
    elif isinstance(value, set):
        return frozenset(value)
    elif isinstance(value, (
            int, float, complex, str, frozenset, type(None),
            ImmutableDict, ImmutableList)):
        return value
    else:
        raise ValueError('Cannot make value of type %s immutable' % type(value))


class ImmutableDict(collections.abc.Mapping):

    def __init__(self, initial={}):
        if isinstance(initial, ImmutableDict):
            self.data = initial.data
        elif isinstance(initial, collections.abc.MutableMapping):
            self.data = self._copy(initial)
        else:
            raise ValueError('Argument `initial` must be a mapping')

    def set(self, key, value):
        if key in self.data and self.data[key] == value:
            return self
        else:
            new = ImmutableDict(self.data)
            new.data[key] = make_immutable(value)
            return new

    def update(self, data):
        if all(key in self.data and self.data[key] == value
               for key, value in data.items()):
            return self

        new_dict = ImmutableDict(self.data)
        new_dict.data.update(data)
        return new_dict

    def delete(self, key):
        new_dict = ImmutableDict(self.data)
        del new_dict.data[key]
        return new_dict

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def __eq__(self, other):
        return isinstance(other, ImmutableDict) and hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return sum(hash(k) + hash(v)
                   for k, v in self.items())

    def _copy(self, data):
        return dict(
            (k, make_immutable(v))
            for k, v in data.items())


class ImmutableList(collections.abc.Sequence):

    def __init__(self, initial=[]):
        if isinstance(initial, ImmutableList):
            self.data = initial.data
        elif isinstance(initial, collections.abc.MutableSequence):
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
