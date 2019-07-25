import re


def pytest_itemcollected(item):
    parent = item.parent.obj
    node = item.obj
    prefix = '{} [{}]'.format(
        parent.__doc__.strip() if parent.__doc__ else parent.__class__.__name__,
        node.__module__
    )
    suffix = node.__doc__.strip() if node.__doc__ else format_description(node.__name__)
    if prefix or suffix:
        item._nodeid = ' '.join((prefix, suffix))


def format_description(test_function_name):
    fn_name_without_prefix = re.sub(r'^test_+', '', test_function_name)
    parts = fn_name_without_prefix.split('__', 1)
    if len(parts) == 1:
        return parts[0]

    return '{} {}'.format(
        parts[0],
        parts[1].replace('_', ' ')
    )
