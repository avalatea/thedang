import pytest
from thedang.rules.tmux import match, get_new_command
from thedang.types import Command


@pytest.fixture
def tmux_ambiguous():
    return "ambiguous command: list, could be: " \
           "list-buffers, list-clients, list-commands, list-keys, " \
           "list-panes, list-sessions, list-windows"


def test_match(tmux_ambiguous):
    assert match(Command('tmux list', tmux_ambiguous))


def test_get_new_command(tmux_ambiguous):
    assert get_new_command(Command('tmux list', tmux_ambiguous))\
        == ['tmux list-keys', 'tmux list-panes', 'tmux list-windows']
