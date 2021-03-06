from configparser import ConfigParser

import pytest
from pyrsistent import pvector

from nete.services import config_storage
from nete.state.models import (
    Configuration,
    NoteCollection,
)


@pytest.fixture
def config():
    return {
        'note-collection-be69fde3-afd7-48b7-9117-c6d34cbe3d1d': {
            'name': 'COLLECTION 1',
            'directory': '/tmp/collection1',
        },
        'note-collection-f6c15221-84c6-45c3-8b7a-30c243994401': {
            'name': 'COLLECTION 2',
            'directory': '/tmp/collection2',
        },
    }


@pytest.fixture
def config_state():
    return Configuration(
        note_collections=pvector([
            NoteCollection(
                id='be69fde3-afd7-48b7-9117-c6d34cbe3d1d',
                name='COLLECTION 1',
                directory='/tmp/collection1'
            ),
            NoteCollection(
                id='f6c15221-84c6-45c3-8b7a-30c243994401',
                name='COLLECTION 2',
                directory='/tmp/collection2'
            ),
        ])
    )


def test__config_to_state__converts_parsed_config_to_state_object(config, config_state):
    config_parser = ConfigParser()
    config_parser.read_dict(config)

    result = config_storage.config_to_state(config_parser)

    assert result == config_state


def test__state_to_config__converts_state_object_to_config_object(config_state, config):
    result = config_storage.state_to_config(config_state)

    assert result == config
