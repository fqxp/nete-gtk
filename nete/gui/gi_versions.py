import gi


def assert_gi_versions():
    gi.require_version('Gtk', '3.0')
    gi.require_version('WebKit2', '4.0')
    gi.require_version('GtkSource', '4')
