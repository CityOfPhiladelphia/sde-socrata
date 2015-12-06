"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from sdesocrata import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=sdesocrata', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'sdesocrata',
    version = __version__,
    description = 'Push Arc SDE tables to Socrata via DataSync',
    long_description = long_description,
    url = 'https://github.com/timwis/sde-socrata',
    author = 'Tim Wisniewski',
    author_email = 'tim@timwis.com',
    license = 'MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'sdesocrata=sdesocrata.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)