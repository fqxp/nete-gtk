from inspect import getargspec


def set_props(component, props):
    component.freeze_notify()
    for key, value in props:
        if component.get_property(key) != value:
            component.set_property(key, value)
    component.thaw_notify()


def connect(Component, map_state_to_props, map_dispatch_to_props=lambda dispatch: {}):

    def create_component(store, *args, **kwargs):
        if 'build_component' in getargspec(Component).args:
            build_component = lambda ChildComponent: ChildComponent(
                store=store)
            component = Component(*args, build_component=build_component, **kwargs)
        else:
            component = Component(*args, **kwargs)

        # connect GObject signals to handlers
        for signal, signal_handler in map_dispatch_to_props(store.dispatch).items():
            # GI isn’t able to handle variable argument lists, so we’re passing
            # an optional list of a maximum number of arguments. The signal
            # handler is provided as a default argument - this is a way to pass
            # a changing reference from the current context to the function
            # we’re defining.
            def handler(source, arg0=None, arg1=None, arg2=None, arg3=None, signal_handler=signal_handler):
                args_count = signal_handler.__code__.co_argcount
                handler_args = [arg0, arg1, arg2, arg3][:args_count]
                signal_handler(*handler_args)
            component.connect(signal, handler)

        # subscribe properties to state changes
        def set_state(state):
            set_props(component, map_state_to_props(state))
        set_state(store.state)
        store.subscribe(set_state)

        return component

    return create_component
