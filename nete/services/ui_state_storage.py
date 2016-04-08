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
    with open(config_filename()) as f:
        config.read_file(f)

    general = config['general']
    geometry = config['window-geometry']
    return {
        'current_note_id': general['current_note_id'],
        'window_position': [geometry.getint('x'), geometry.getint('y')],
        'window_size': [geometry.getint('width'), geometry.getint('height')],
    }


def save_ui_state(ui_state):
    config = ConfigParser()

    config['general'] = {}
    config['general']['current_note_id'] = ui_state['current_note_id'] or ''

    config['window-geometry'] = {}
    config['window-geometry']['width'] = str(ui_state['window_size'][0])
    config['window-geometry']['height'] = str(ui_state['window_size'][1])
    window_position = ui_state['window_position']
    config['window-geometry']['x'] = str(window_position[0]) if window_position is not None else ''
    config['window-geometry']['y'] = str(window_position[1]) if window_position is not None else ''

    with open(config_filename(), 'w') as config_file:
        config.write(config_file)


def config_filename():
    if 'NETE_DIR' in os.environ:
        basedir = os.environ['NETE_DIR']
    elif 'XDG_CONFIG_HOME' in os.environ:
        basedir = os.path.join(os.environ['XDG_CONFIG_HOME'], 'nete')
    else:
        basedir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'nete')

    return os.path.join(basedir, CONFIG_FILENAME)
