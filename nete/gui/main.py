import sys

from nete.gui import gi_versions
from nete.gui.application import Application
from nete.gui.resources import (
    sourceview_languages_dir,
    sourceview_styles_dir,
)
from gi.repository import Gtk, GtkSource


def main():
    setup_gtk()

    app = Application()
    exit_status = app.run(sys.argv)

    Gtk.main()

    sys.exit(exit_status)


def setup_gtk():
    language_manager = GtkSource.LanguageManager.get_default()
    language_manager.set_search_path(
        language_manager.get_search_path() +
        [sourceview_languages_dir()])

    style_scheme_manager = GtkSource.StyleSchemeManager.get_default()
    style_scheme_manager.append_search_path(sourceview_styles_dir())
