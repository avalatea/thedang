from thedang.shells import shell
from thedang.utils import for_app


@for_app('tsuru')
def match(command):
    return ('not authenticated' in command.output
            and 'session has expired' in command.output)


def get_new_command(command):
    return shell.and_('tsuru login', command.script)
