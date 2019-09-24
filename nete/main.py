import sys

from nete.gi_versions import assert_gi_versions
assert_gi_versions()
from nete.application import Application
from nete.resources import (
    sourceview_languages_dir,
    sourceview_styles_dir,
)
from gi.repository import Gtk, GtkSource


def main():
    setup_gtk()

    try:
        app = Application()
        sys.exit(app.run(sys.argv))
    except KeyboardInterrupt:
        sys.exit(0)


def setup_gtk():
    language_manager = GtkSource.LanguageManager.get_default()
    language_manager.set_search_path(
        language_manager.get_search_path()
        + [sourceview_languages_dir()])

    style_scheme_manager = GtkSource.StyleSchemeManager.get_default()
    style_scheme_manager.append_search_path(sourceview_styles_dir())
