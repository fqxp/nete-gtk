class Store:
    def __init__(self, reducer, initial_state):
        self._reducer = reducer
        self._state = initial_state
        self._listeners = {}

    @property
    def state(self):
        return self._state

    def dispatch(self, action):
        while callable(action):
            action = action(self.dispatch, self._state)

        if action is None:
            return

        prev_state = self._state
        self._state = self._reducer(self._state, action)

        if prev_state is self._state:
            return

        self._inform_listeners(prev_state, self._state)

    def subscribe(self, listener, selector=lambda state: state):
        if selector not in self._listeners:
            self._listeners[selector] = []
        self._listeners[selector].append(listener)

    def _inform_listeners(self, old_state, new_state):
        for selector, listeners in self._listeners.items():
            selected_old_state = selector(old_state)
            selected_new_state = selector(new_state)

            if selected_old_state == selected_new_state:
                continue

            for listener in listeners:
                listener(selected_new_state, self.dispatch)
