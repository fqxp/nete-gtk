def identity(v):
    return v


def create_component(Component, store, map_state_to_props,
                     *args, selector=identity, **kwargs):
    component = Component(*args, **kwargs)

    def on_state_changed(selected_state):
        for property_name, value in map_state_to_props(selected_state):
            if value != component.get_property(property_name):
                component.set_property(property_name, value)

    subscription = store.map(selector).subscribe(on_state_changed)

    def on_destroy(*args):
        print('DISPOSE %r' % component)
        subscription.dispose()

    component.connect('destroy', on_destroy)

    return component
