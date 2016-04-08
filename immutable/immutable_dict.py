import collections.abc
from .functions import make_immutable, set_by_path


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

    def set_by_path(self, path, value):
        return set_by_path(self, path, value)

    def update(self, data):
        if all(key in self.data and self.data[key] == value
               for key, value in data.items()):
            return self

        new_dict = ImmutableDict(self.data)
        new_dict.data.update(make_immutable(data))
        return new_dict

    def delete(self, key):
        new_dict = ImmutableDict(self.data)
        del new_dict.data[key]
        return new_dict

    def mutable(self):
        return {key: value.mutable() if hasattr(value, 'mutable') else value
                for key, value in self.data.items()}

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

    def __str__(self):
        return '{%s}' % ', '.join(map(lambda kv: '%r: %s' % (kv[0], str(kv[1])),
                            self.data.items()))
