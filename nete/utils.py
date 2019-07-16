import pkg_resources


def version():
    dist = pkg_resources.get_distribution('nete')
    return dist.version


def in_development_mode():
    return version().endswith('dev')
