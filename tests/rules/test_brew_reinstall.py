import pytest
from thedang.types import Command
from thedang.rules.brew_reinstall import get_new_command, match


output = ("Warning: thedang 9.9 is already installed and up-to-date\nTo "
          "reinstall 9.9, run `brew reinstall thedang`")


def test_match():
    command = Command('brew install thedang', output)
    assert match(command)


@pytest.mark.parametrize('script', [
    'brew reinstall thedang',
    'brew install foo'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, formula, ', [
    ('brew install foo', 'foo'),
    ('brew install bar zap', 'bar zap')])
def test_get_new_command(script, formula):
    command = Command(script, output)
    new_command = 'brew reinstall {}'.format(formula)
    assert get_new_command(command) == new_command
