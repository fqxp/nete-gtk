def set_props(component, props):
    for key, value in props.items():
        if component.get_property(key) != props[key]:
            component.set_property(key, value)


def connect(Component, map_state_to_props, map_dispatch_to_props={}):

    def create_component(store, *args, **kwargs):
        component = Component()

        # connect GObject signals to handlers
        for signal, signal_handler in map_dispatch_to_props(store.dispatch).items():
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