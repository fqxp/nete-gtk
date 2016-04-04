from configparser import ConfigParser
import os
import os.path

CONFIG_FILENAME = 'nete.conf'

__all__ = (
    'load_ui_state',
    'save_ui_state',
)


def load_ui_state():
    config = ConfigParser()
    config.read(config_filename())

    geometry = config['window-geometry']
    return {
        'window_position': [geometry.getint('x'), geometry.getint('y')],
        'window_size': [geometry.getint('width'), geometry.getint('height')],
    }


def save_ui_state(ui_state):
    config = ConfigParser()
    x, y = ui_state['window_position']
    width, height = ui_state['window_size']
    config['window-geometry'] = {
        'x': x,
        'y': y,
        'width': width,
        'height': height,
    }

    with open(config_filename(), 'w') as config_file:
        print('WRITING: %r' % dict(config['window-geometry']))
        config.write(config_file)


def config_filename():
    if 'NETE_DIR' in os.environ:
        basedir = os.environ['NETE_DIR']
    elif 'XDG_CONFIG_HOME' in os.environ:
        basedir = os.path.join(os.environ['XDG_CONFIG_HOME'], 'nete')
    else:
        basedir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'nete')

    return os.path.join(basedir, CONFIG_FILENAME)
