import collections
import types


def make_immutable(value):
    from .immutable_dict import ImmutableDict
    from .immutable_list import ImmutableList

    if isinstance(value, collections.MutableMapping):
        return ImmutableDict(value)
    elif (isinstance(value, collections.MutableSequence) or
          isinstance(value, types.GeneratorType)):
        return ImmutableList(value)
    elif isinstance(value, set):
        return frozenset(value)
    elif isinstance(value, (
            int, float, complex, str, frozenset, type(None),
            ImmutableDict, ImmutableList)):
        return value
    else:
        raise ValueError('Cannot make value of type %s immutable' % type(value))


def get_by_path(container, path):
    if len(path) == 0:
        raise KeyError('path must have at least one element')

    key = path[0]

    if len(path) == 1:
        return container[key]
    else:
        rest = path[1:]
        return get_by_path(container[key], rest)


def set_by_path(container, path, new_value):
    if len(path) == 0:
        raise KeyError('path must have at least one element')

    key = path[0]

    if len(path) == 1:
        return container.set(key, new_value)
    else:
        child_container = container[key]
        rest = path[1:]
        new_value = set_by_path(child_container, rest, new_value)
        return container.set(key, new_value)
