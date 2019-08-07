import pytest
import random

from nete.gui.services.markdown import markdown


@pytest.fixture
def mock_random(monkeypatch):
    monkeypatch.setattr(
        random,
        'randint',
        lambda min, max: 123)


def test__markdown__renders_checkbox(mock_random):
    result = markdown('[ ] FOO')

    assert result == (
        '<div class="checkbox checkbox__level_1">'
        '  <input type="checkbox" id="123" onclick="return false" >'
        '  <label for="123">FOO</label>'
        '</div>')


def test__markdown__renders_checked_checkbox(mock_random):
    result = markdown('[x] FOO')

    assert result == (
        '<div class="checkbox checkbox__level_1">'
        '  <input type="checkbox" id="123" onclick="return false" checked>'
        '  <label for="123">FOO</label>'
        '</div>')


def test__markdown__renders_indented_checkboxes(mock_random):
    result = markdown('[ ] FOO\n  [ ] BAR')

    assert result == (
        '<div class="checkbox checkbox__level_1">'
        '  <input type="checkbox" id="123" onclick="return false" >'
        '  <label for="123">FOO</label>'
        '</div>'
        '<div class="checkbox checkbox__level_2">'
        '  <input type="checkbox" id="123" onclick="return false" >'
        '  <label for="123">BAR</label>'
        '</div>'
    )
