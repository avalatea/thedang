import pytest
from thedang.rules.brew_unknown_command import match, get_new_command
from thedang.rules.brew_unknown_command import _brew_commands
from thedang.types import Command


@pytest.fixture
def brew_unknown_cmd():
    return '''Error: Unknown command: inst'''


@pytest.fixture
def brew_unknown_cmd2():
    return '''Error: Unknown command: instaa'''


def test_match(brew_unknown_cmd):
    assert match(Command('brew inst', brew_unknown_cmd))
    for command in _brew_commands():
        assert not match(Command('brew ' + command, ''))


def test_get_new_command(brew_unknown_cmd, brew_unknown_cmd2):
    assert (get_new_command(Command('brew inst', brew_unknown_cmd))
            == ['brew list', 'brew install', 'brew uninstall'])

    cmds = get_new_command(Command('brew instaa', brew_unknown_cmd2))
    assert 'brew install' in cmds
    assert 'brew uninstall' in cmds
