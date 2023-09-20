import pytest
from thedang.argument_parser import Parser
from thedang.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['thedang'], _args()),
    (['thedang', '-a'], _args(alias='dang')),
    (['thedang', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='dang', enable_experimental_instant_mode=True)),
    (['thedang', '-a', 'fix'], _args(alias='fix')),
    (['thedang', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['thedang', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['thedang', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['thedang', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['thedang', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['thedang', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['thedang', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['thedang', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
