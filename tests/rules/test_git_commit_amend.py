import pytest
from thedang.rules.git_commit_amend import match, get_new_command
from thedang.types import Command


@pytest.mark.parametrize('script, output', [
    ('git commit -m "test"', 'test output'),
    ('git commit', '')])
def test_match(output, script):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git branch foo',
    'git checkout feature/test_commit',
    'git push'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script', [
    ('git commit -m "test commit"'),
    ('git commit')])
def test_get_new_command(script):
    assert get_new_command(Command(script, '')) == 'git commit --amend'
