from rx.subjects import BehaviorSubject


class Store(BehaviorSubject):

    def __init__(self, initial_state):
        super().__init__(initial_state)


