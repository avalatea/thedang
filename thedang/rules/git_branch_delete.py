from thedang.utils import replace_argument
from thedang.specific.git import git_support


@git_support
def match(command):
    return ('branch -d' in command.script
            and 'If you are sure you want to delete it' in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, '-d', '-D')
