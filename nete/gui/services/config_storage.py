import logging
import os
import os.path
from configparser import ConfigParser

from pyrsistent import PSet, s

from nete.gui.state.models import Configuration, NoteCollection
from nete.utils import config_filename

CONFIG_FILENAME = 'config.ini'
NOTE_COLLECTION_PREFIX = 'note-collection-'


logger = logging.getLogger(__name__)


def load_configuration():
    if not os.path.exists(config_filename(CONFIG_FILENAME)):
        save_configuration(default_configuration())

    logger.debug('Loading configuration from {}'.format(
        config_filename(CONFIG_FILENAME)))

    config_parser = ConfigParser()
    config_parser.read(config_filename(CONFIG_FILENAME))

    return config_to_state(config_parser)


def save_configuration(configuration):
    logger.debug('Saving configuration to {}'.format(
        config_filename(CONFIG_FILENAME)))

    filename = config_filename(CONFIG_FILENAME)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    config_parser = ConfigParser()
    config_parser.read_dict(state_to_config(configuration))
    config_parser.write(open(filename, 'w'))


def config_to_state(config):
    return Configuration(
        note_collections=PSet(
            NoteCollection(
                id=collection_id,
                name=collection_config['name'],
                directory=collection_config['directory']
            )
            for (collection_id, collection_config)
            in _note_collection_configs(config)
        )
    )


def _note_collection_configs(config):
    return (
        (section[len(NOTE_COLLECTION_PREFIX):], config[section])
        for section in config.sections()
        if section.startswith(NOTE_COLLECTION_PREFIX)
    )


def state_to_config(state):
    return {
        '{}{}'.format(NOTE_COLLECTION_PREFIX, note_collection.id): {
            'name': note_collection.name,
            'directory': note_collection.directory,
        }
        for note_collection in state.note_collections
    }


def default_configuration():
    note_collections = s(
        NoteCollection(
            id='630415b9-290e-4b3e-94d3-c96bca7b9694',
            name='Personal',
            directory=os.path.join(
                os.path.expanduser('~'),
                'Notes'
            )
        ),
    )

    return Configuration(
        note_collections=note_collections,
    )
