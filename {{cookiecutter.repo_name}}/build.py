#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from subprocess import call

from flask.ext.script import Manager, Server
from flask.ext.script.commands import ShowUrls, Clean
from app import create_app
from nose.core import run

env = os.environ.get('APP_ENV', 'development')
app = create_app('app.config.settings.{0}.{1}Config'.format(env.lower(), env.capitalize()), env=env)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.command
def lint():
    """
    Run linter on our code base.
    """
    path = os.path.realpath(os.getcwd())
    cmd = 'flake8 {0}' .format(path)
    opt = ''
    print(">>> Linting codebase with the following command: {0} {1}".format(cmd, opt))

    try:
        return_code = call([cmd, opt], shell=True)
        if return_code < 0:
            print(">>> Terminated by signal", -return_code, file=sys.stderr)
        elif return_code != 0:
            sys.exit('>>> Lint checks failed')
        else:
            print(">>> Lint checks passed")
    except OSError as e:
        print(">>> Execution failed:", e, file=sys.stderr)


@manager.command
def unit_tests(extra_args=[]):
    """
    Run unit tests for this code base. Pass any arguments that nose accepts.

    '--cover-html' to get html output

    :argument list extra_args: List of extra arguments
    """
    path = os.path.realpath(os.path.join(os.getcwd(), 'tests/unit'))
    args = ['-x', '-v', '--with-coverage', '--cover-erase', '--cover-package=./app', path]

    if extra_args:
        args.extend(extra_args)

    if run(argv=args):
        return 0
    else:
        return 1


@manager.command
def integration_tests(extra_args=[]):
    """
    Run unit tests for this code base. Pass any arguments that nose accepts.

    :argument list extra_args: List of extra arguments
    """
    path = os.path.realpath(os.path.join(os.getcwd(), 'tests/integration/'))
    args = ['-x', '-v', '--with-coverage', '--cover-erase', '--cover-package=./app', path]

    if extra_args:
        args.extend(extra_args)

    if run(argv=args):
        return 0
    else:
        return 1


@manager.command
def test_suite():
    """
    Run both unit test and lint with default args
    """
    lint()
    unit_tests()
    integration_tests()


if __name__ == "__main__":
    manager.run()
