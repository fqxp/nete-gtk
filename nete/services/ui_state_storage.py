from configparser import ConfigParser
import logging
import os
import os.path

from nete.utils import config_filename

CONFIG_FILENAME = 'nete.conf'

__all__ = (
    'load_ui_state',
    'save_ui_state',
)

logger = logging.getLogger(__name__)


def load_ui_state():
    config = ConfigParser()

    if not os.path.exists(config_filename(CONFIG_FILENAME)):
        return {}

    with open(config_filename(CONFIG_FILENAME)) as f:
        config.read_file(f)

    result = {}
    general = config['general']
    if 'current_note_id' in general:
        result['current_note_id'] = general['current_note_id']
    if 'paned-position' in general:
        result['paned_position'] = int(general['paned-position'])

    return result


def save_ui_state(ui_state):
    config = ConfigParser()

    config['general'] = {}
    config['general']['paned-position'] = str(ui_state['paned_position'])

    os.makedirs(os.path.dirname(config_filename(CONFIG_FILENAME)), exist_ok=True)
    with open(config_filename(CONFIG_FILENAME), 'w') as config_file:
        config.write(config_file)

    logger.debug('Saved UI state')
