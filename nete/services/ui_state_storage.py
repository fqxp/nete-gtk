from configparser import ConfigParser
import logging
import os
import os.path

CONFIG_FILENAME = 'nete.conf'

__all__ = (
    'load_ui_state',
    'save_ui_state',
)

logger = logging.getLogger(__name__)


def load_ui_state():
    config = ConfigParser()
    with open(config_filename()) as f:
        config.read_file(f)

    general = config['general']
    result = {}
    if 'current_note_id' in general:
        result['current_note_id'] = general['current_note_id']
    if 'paned-position' in general:
        result['paned_position'] = int(general['paned-position'])

    return result


def save_ui_state(ui_state):
    config = ConfigParser()

    config['general'] = {}
    config['general']['current_note_id'] = ui_state['current_note_id'] or ''
    config['general']['paned-position'] = str(ui_state['paned_position'])

    with open(config_filename(), 'w') as config_file:
        config.write(config_file)

    logger.debug('Saved UI state')


def config_filename():
    if 'NETE_DIR' in os.environ:
        basedir = os.environ['NETE_DIR']
    elif 'XDG_CONFIG_HOME' in os.environ:
        basedir = os.path.join(os.environ['XDG_CONFIG_HOME'], 'nete')
    else:
        basedir = os.path.join(os.path.expanduser('~'), '.local', 'share', 'nete')

    return os.path.join(basedir, CONFIG_FILENAME)
