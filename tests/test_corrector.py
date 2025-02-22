# -*- coding: utf-8 -*-

import pytest
from tests.utils import Rule, CorrectedCommand
from thedang import corrector, const
from thedang.system import Path
from thedang.types import Command
from thedang.corrector import get_corrected_commands, organize_commands


@pytest.fixture
def glob(mocker):
    results = {}
    mocker.patch('thedang.system.Path.glob',
                 new_callable=lambda: lambda *_: results.pop('value', []))
    return lambda value: results.update({'value': value})


class TestGetRules(object):
    @pytest.fixture(autouse=True)
    def load_source(self, monkeypatch):
        monkeypatch.setattr('thedang.types.load_source',
                            lambda x, _: Rule(x))

    def _compare_names(self, rules, names):
        assert {r.name for r in rules} == set(names)

    @pytest.mark.parametrize('paths, conf_rules, exclude_rules, loaded_rules', [
        (['git.py', 'bash.py'], const.DEFAULT_RULES, [], ['git', 'bash']),
        (['git.py', 'bash.py'], ['git'], [], ['git']),
        (['git.py', 'bash.py'], const.DEFAULT_RULES, ['git'], ['bash']),
        (['git.py', 'bash.py'], ['git'], ['git'], [])])
    def test_get_rules(self, glob, settings, paths, conf_rules, exclude_rules,
                       loaded_rules):
        glob([Path(path) for path in paths])
        settings.update(rules=conf_rules,
                        priority={},
                        exclude_rules=exclude_rules)
        rules = corrector.get_rules()
        self._compare_names(rules, loaded_rules)


def test_get_rules_rule_exception(mocker, glob):
    load_source = mocker.patch('thedang.types.load_source',
                               side_effect=ImportError("No module named foo..."))
    glob([Path('git.py')])
    assert not corrector.get_rules()
    load_source.assert_called_once_with('git', 'git.py')


def test_get_corrected_commands(mocker):
    command = Command('test', 'test')
    rules = [Rule(match=lambda _: False),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: x.script + '!', priority=100),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: [x.script + '@', x.script + ';'],
                  priority=60)]
    mocker.patch('thedang.corrector.get_rules', return_value=rules)
    assert ([cmd.script for cmd in get_corrected_commands(command)]
            == ['test!', 'test@', 'test;'])


def test_organize_commands():
    """Ensures that the function removes duplicates and sorts commands."""
    commands = [CorrectedCommand('ls'), CorrectedCommand('ls -la', priority=9000),
                CorrectedCommand('ls -lh', priority=100),
                CorrectedCommand(u'echo café', priority=200),
                CorrectedCommand('ls -lh', priority=9999)]
    assert list(organize_commands(iter(commands))) \
        == [CorrectedCommand('ls'), CorrectedCommand('ls -lh', priority=100),
            CorrectedCommand(u'echo café', priority=200),
            CorrectedCommand('ls -la', priority=9000)]
