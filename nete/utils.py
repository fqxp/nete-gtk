import pkg_resources


def in_development_mode():
    dist = pkg_resources.get_distribution('nete')
    return dist.version.endswith('dev')
