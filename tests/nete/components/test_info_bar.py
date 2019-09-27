import os
import time

import pytest
from gi.repository import Gtk, GLib

from nete.components.info_bar import InfoBar

__doc__ = 'InfoBar'


@pytest.fixture
def info_bar():
    return InfoBar()


@pytest.fixture
def info_bar_with_1_second_reveal_timeout(info_bar):
    info_bar.REVEAL_TIMEOUT = 1

    return info_bar


@pytest.fixture
def refresh_gui():
    def refresh_gui():
        GLib.MainContext.default().acquire()
        GLib.MainContext.default().dispatch()
        GLib.MainContext.default().release()

        while Gtk.events_pending():
            Gtk.main_iteration_do(blocking=False)
    return refresh_gui


def test__changing_info_message_reveals_info_bar(info_bar):
    assert not info_bar.props.revealed

    info_bar.props.info_message = 'FOO'

    assert info_bar.props.revealed


def test__changing_info_message_updates_label(info_bar):
    assert info_bar.label.props.label != 'FOO'

    info_bar.props.info_message = 'FOO'

    assert info_bar.label.props.label == 'FOO'


@pytest.mark.skipif(
    'TRAVIS' in os.environ,
    reason='this one’s flaky anyway, but even more on Travis CI '
    'because we cannot depend on accurate timing')
def test__info_bar_is_hidden_after_x_seconds(
    info_bar_with_1_second_reveal_timeout,
    refresh_gui
):
    info_bar_with_1_second_reveal_timeout.props.info_message = 'FOO'

    assert info_bar_with_1_second_reveal_timeout.props.revealed

    time.sleep(2)
    refresh_gui()

    assert not info_bar_with_1_second_reveal_timeout.props.revealed


@pytest.mark.skipif(
    'TRAVIS' in os.environ,
    reason='this one’s flaky anyway, but even more on Travis CI '
    'because we cannot depend on accurate timing')
def test__info_bar_reveal_timeout_is_extended_when_there_are_two_updates(
    info_bar_with_1_second_reveal_timeout,
    refresh_gui
):
    info_bar_with_1_second_reveal_timeout.props.info_message = 'FOO'

    assert info_bar_with_1_second_reveal_timeout.props.revealed

    time.sleep(1)
    refresh_gui()

    info_bar_with_1_second_reveal_timeout.props.info_message = 'BAR'

    time.sleep(1)
    refresh_gui()

    assert info_bar_with_1_second_reveal_timeout.props.revealed

    time.sleep(1)
    refresh_gui()

    assert not info_bar_with_1_second_reveal_timeout.props.revealed
