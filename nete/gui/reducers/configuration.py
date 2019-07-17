from fluous import create_reducer

from nete.gui.actions.action_types import ActionType


reduce = create_reducer({
    ActionType.LOAD_CONFIGURATION: lambda state, action: (
        action['configuration']
    ),
})
