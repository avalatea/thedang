from thedang.utils import replace_argument
from thedang.specific.git import git_support


@git_support
def match(command):
    return ('tag' in command.script_parts
            and 'already exists' in command.output)


@git_support
def get_new_command(command):
    return replace_argument(command.script, 'tag', 'tag --force')
