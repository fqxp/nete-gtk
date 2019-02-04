from inspect import getargspec
from contextlib import contextmanager

__all__ = ('connect', )

silenced_notify_signals = []


def connect(Component, map_state_to_props=lambda state: tuple(), map_dispatch_to_props=lambda dispatch: {}):

    def create_component(store, *args, **kwargs):
        initial_properties = {key.replace('-', '_'): value
                              for (key, value) in map_state_to_props(store.state)}
        component_kwargs = {**initial_properties, **kwargs}

        if 'build_component' in getargspec(Component).args:
            build_component = lambda ChildComponent: ChildComponent(
                store=store)
            component = Component(*args, build_component=build_component, **component_kwargs)
        else:
            component = Component(*args, **component_kwargs)

        # connect GObject signals to handlers
        for signal, signal_handler in map_dispatch_to_props(store.dispatch).items():
            # GI isn’t able to handle variable argument lists, so we’re passing
            # an optional list of a maximum number of arguments. The signal
            # handler is provided as a default argument - this is a way to pass
            # a changing reference from the current context to the function
            # we’re defining.
            def handler(source, arg0=None, arg1=None, arg2=None, arg3=None, signal=signal, signal_handler=signal_handler):
                if is_notify_signal_silenced(source, signal):
                    return

                args_count = signal_handler.__code__.co_argcount
                handler_args = [source, arg0, arg1, arg2, arg3][:args_count]
                signal_handler(*handler_args)

            component.connect(signal, handler)

        # subscribe properties to state changes
        def set_state(state):
            set_properties(component, map_state_to_props(state))
        set_state(store.state)
        store.subscribe(lambda state, _: set_state(state))

        return component

    return create_component


def set_properties(component, properties):
    for property_name, value in properties:
        property_value = component.get_property(property_name)

        if property_value != value:
            with silence_notify_signal(component, property_name):
                component.set_property(property_name, value)


@contextmanager
def silence_notify_signal(source, property_name):
    global silenced_notify_signals
    silenced_notify_signals.append((source, 'notify::{}'.format(property_name)))
    yield
    silenced_notify_signals.pop()


def is_notify_signal_silenced(source, signal):
    global silenced_notify_signals
    return signal.startswith('notify::') and (source, signal) in silenced_notify_signals
