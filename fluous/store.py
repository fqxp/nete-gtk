from fluous.immutable import ImmutableDict


class Store:
    def __init__(self, reducer, initial_state={}):
        self._reducer = reducer
        self._state = ImmutableDict(initial_state)
        self._listeners = []

    @property
    def state(self):
        return self._state

    def dispatch(self, action):
        if action is None:
            return

        if callable(action):
            action = action(self.dispatch, self._state)

        prev_state = self._state
        self._state = self._reducer(self._state, action)

        if prev_state is self._state:
            return

        for listener in self._listeners:
            listener(self._state)

    def subscribe(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener):
        if listener in self._listeners:
            self._listeners.remove(listener)
