import pytest
from thedang.rules.git_clone_missing import match, get_new_command
from thedang.types import Command

valid_urls = [
    'https://github.com/nvbn/thedang.git',
    'https://github.com/nvbn/thedang',
    'http://github.com/nvbn/thedang.git',
    'git@github.com:nvbn/thedang.git',
    'git@github.com:nvbn/thedang',
    'ssh://git@github.com:nvbn/thedang.git',
]
invalid_urls = [
    '',  # No command
    'notacommand',  # Command not found
    'ssh git@github.com:nvbn/thefrick.git',  # ssh command, not a git clone
    'git clone foo',  # Valid clone
    'git clone https://github.com/nvbn/thedang.git',  # Full command
    'github.com/nvbn/thedang.git',  # Missing protocol
    'github.com:nvbn/thedang.git',  # SSH missing username
    'git clone git clone ssh://git@github.com:nvbn/thefrick.git',  # 2x clone
    'https:/github.com/nvbn/thedang.git'  # Bad protocol
]
outputs = [
    'No such file or directory',
    'not found',
    'is not recognised as',
]


@pytest.mark.parametrize('cmd', valid_urls)
@pytest.mark.parametrize('output', outputs)
def test_match(cmd, output):
    c = Command(cmd, output)
    assert match(c)


@pytest.mark.parametrize('cmd', invalid_urls)
@pytest.mark.parametrize('output', outputs + ["some other output"])
def test_not_match(cmd, output):
    c = Command(cmd, output)
    assert not match(c)


@pytest.mark.parametrize('script', valid_urls)
@pytest.mark.parametrize('output', outputs)
def test_get_new_command(script, output):
    command = Command(script, output)
    new_command = 'git clone ' + script
    assert get_new_command(command) == new_command
