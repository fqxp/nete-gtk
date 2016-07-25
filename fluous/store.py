from pyrsistent import freeze


class Store:
    def __init__(self, reducer, initial_state={}):
        self._reducer = reducer
        self._state = freeze(initial_state)
        self._listeners = []
        self._middlewares = []

    @property
    def state(self):
        return self._state

    def add_middleware(self, middleware):
        self._middlewares.append(middleware)

    def dispatch(self, action):
        while callable(action):
            action = action(self.dispatch, self._state)

        if action is None:
            return

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
