from nete.gui.actions.action_types import ActionType
from nete.gui.services import config_storage


def load_configuration():
    def load_configuration(dispatch, state):
        configuration = config_storage.load_configuration()

        return {
            'type': ActionType.LOAD_CONFIGURATION,
            'configuration': configuration,
        }
    return load_configuration


def save_configuration():
    def save_configuration(dispatch, state):
        config_storage.save_configuration(state['configuration'])
    return save_configuration
