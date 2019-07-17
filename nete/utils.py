import os
import os.path
import pkg_resources
from functools import lru_cache


def version():
    dist = pkg_resources.get_distribution('nete')
    return dist.version


def in_development_mode():
    return 'dev' in version()


@lru_cache()
def config_filename(filename):
    if 'NETE_DIR' in os.environ:
        basedir = os.environ['NETE_DIR']
    elif 'XDG_CONFIG_HOME' in os.environ:
        basedir = os.path.join(os.environ['XDG_CONFIG_HOME'], 'nete')
    else:
        basedir = os.path.join(os.path.expanduser('~'), '.config', 'nete')

    return os.path.join(basedir, filename)


def find(l, pred):
    matching = [item for item in l if pred(item)]
    if len(matching) == 0:
        return None
    elif len(matching) > 1:
        raise Exception('found more than one match')

    return matching[0]
