from io import BytesIO
import pytest
from thedang.types import Command
from thedang.rules.apt_invalid_operation import match, get_new_command, \
    _get_operations

invalid_operation = 'E: Invalid operation {}'.format
apt_help = b'''apt 1.0.10.2ubuntu1 for amd64 compiled on Oct  5 2015 15:55:05
Usage: apt [options] command

CLI for apt.
Basic commands:
 list - list packages based on package names
 search - search in package descriptions
 show - show package details

 update - update list of available packages

 install - install packages
 remove  - remove packages

 upgrade - upgrade the system by installing/upgrading packages
 full-upgrade - upgrade the system by removing/installing/upgrading packages

 edit-sources - edit the source information file
'''
apt_operations = ['list', 'search', 'show', 'update', 'install', 'remove',
                  'upgrade', 'full-upgrade', 'edit-sources']

apt_get_help = b'''apt 1.0.10.2ubuntu1 for amd64 compiled on Oct  5 2015 15:55:05
Usage: apt-get [options] command
       apt-get [options] install|remove pkg1 [pkg2 ...]
       apt-get [options] source pkg1 [pkg2 ...]

apt-get is a simple command line interface for downloading and
installing packages. The most frequently used commands are update
and install.

Commands:
   update - Retrieve new lists of packages
   upgrade - Perform an upgrade
   install - Install new packages (pkg is libc6 not libc6.deb)
   remove - Remove packages
   autoremove - Remove automatically all unused packages
   purge - Remove packages and config files
   source - Download source archives
   build-dep - Configure build-dependencies for source packages
   dist-upgrade - Distribution upgrade, see apt-get(8)
   dselect-upgrade - Follow dselect selections
   clean - Erase downloaded archive files
   autoclean - Erase old downloaded archive files
   check - Verify that there are no broken dependencies
   changelog - Download and display the changelog for the given package
   download - Download the binary package into the current directory

Options:
  -h  This help text.
  -q  Loggable output - no progress indicator
  -qq No output except for errors
  -d  Download only - do NOT install or unpack archives
  -s  No-act. Perform ordering simulation
  -y  Assume Yes to all queries and do not prompt
  -f  Attempt to correct a system with broken dependencies in place
  -m  Attempt to continue if archives are unlocatable
  -u  Show a list of upgraded packages as well
  -b  Build the source package after fetching it
  -V  Show verbose version numbers
  -c=? Read this configuration file
  -o=? Set an arbitrary configuration option, eg -o dir::cache=/tmp
See the apt-get(8), sources.list(5) and apt.conf(5) manual
pages for more information and options.
                       This APT has Super Cow Powers.
'''
apt_get_operations = ['update', 'upgrade', 'install', 'remove', 'autoremove',
                      'purge', 'source', 'build-dep', 'dist-upgrade',
                      'dselect-upgrade', 'clean', 'autoclean', 'check',
                      'changelog', 'download']

new_apt_get_help = b'''apt 1.6.12 (amd64)
Usage: apt-get [options] command
       apt-get [options] install|remove pkg1 [pkg2 ...]
       apt-get [options] source pkg1 [pkg2 ...]

apt-get is a command line interface for retrieval of packages
and information about them from authenticated sources and
for installation, upgrade and removal of packages together
with their dependencies.

Most used commands:
  update - Retrieve new lists of packages
  upgrade - Perform an upgrade
  install - Install new packages (pkg is libc6 not libc6.deb)
  remove - Remove packages
  purge - Remove packages and config files
  autoremove - Remove automatically all unused packages
  dist-upgrade - Distribution upgrade, see apt-get(8)
  dselect-upgrade - Follow dselect selections
  build-dep - Configure build-dependencies for source packages
  clean - Erase downloaded archive files
  autoclean - Erase old downloaded archive files
  check - Verify that there are no broken dependencies
  source - Download source archives
  download - Download the binary package into the current directory
  changelog - Download and display the changelog for the given package

See apt-get(8) for more information about the available commands.
Configuration options and syntax is detailed in apt.conf(5).
Information about how to configure sources can be found in sources.list(5).
Package and version choices can be expressed via apt_preferences(5).
Security details are available in apt-secure(8).
                                        This APT has Super Cow Powers.
'''
new_apt_get_operations = ['update', 'upgrade', 'install', 'remove', 'purge',
                          'autoremove', 'dist-upgrade', 'dselect-upgrade',
                          'build-dep', 'clean', 'autoclean', 'check',
                          'source', 'download', 'changelog']


@pytest.mark.parametrize('script, output', [
    ('apt', invalid_operation('saerch')),
    ('apt-get', invalid_operation('isntall')),
    ('apt-cache', invalid_operation('rumove'))])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('script, output', [
    ('vim', invalid_operation('vim')),
    ('apt-get', "")])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.fixture
def set_help(mocker):
    mock = mocker.patch('subprocess.Popen')

    def _set_text(text):
        mock.return_value.stdout = BytesIO(text)

    return _set_text


@pytest.mark.parametrize('app, help_text, operations', [
    ('apt', apt_help, apt_operations),
    ('apt-get', apt_get_help, apt_get_operations),
    ('apt-get', new_apt_get_help, new_apt_get_operations)
])
def test_get_operations(set_help, app, help_text, operations):
    set_help(help_text)
    assert _get_operations(app) == operations


@pytest.mark.parametrize('script, output, help_text, result', [
    ('apt-get isntall vim', invalid_operation('isntall'),
     apt_get_help, 'apt-get install vim'),
    ('apt saerch vim', invalid_operation('saerch'),
     apt_help, 'apt search vim'),
    ('apt uninstall vim', invalid_operation('uninstall'),
     apt_help, 'apt remove vim'),
])
def test_get_new_command(set_help, output, script, help_text, result):
    set_help(help_text)
    assert get_new_command(Command(script, output))[0] == result
