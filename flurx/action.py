from rx.subjects import Subject
from functools import wraps


def action(f):
    return Action(f)


class Action(Subject):

    def __init__(self, action_func):
        super().__init__()
        self.action_func = action_func

    def __call__(self, *args, **kwargs):
        action_params = self.action_func(*args, **kwargs)
        self.on_next(action_params)
