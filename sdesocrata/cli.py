"""
sdesocrata

Usage:
  sdesocrata create <table> [--public] [--config=<config_path>]
  sdesocrata push <table> <id>
  sdesocrata push --list=<list_path>
  sdesocrata -h | --help
  sdesocrata --version

Options:
  --public                          Set dataset permissions to public
  --config=<config_path>            Path to config file [default: ./config/config.json]
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  sdesocrata create Council_Districts_2016
  sdesocrata push Council_Districts_2016 jo21-8sz0
  sdesocrata push --list=config/datasets.yaml

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/timwis/sde-socrata
"""

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    for k, v in options.iteritems():
        if hasattr(commands, k):
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()