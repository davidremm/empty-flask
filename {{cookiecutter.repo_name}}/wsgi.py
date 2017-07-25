# -*- coding: utf-8 -*-
import sys
import os

from flask.ext.cors import CORS

from app.{{ cookiecutter.repo_name }} import create_app

project = '{{ cookiecutter.repo_name }}'

# Use instance folder, instead of env variables.
# specify dev/production config
# os.environ['%s_APP_CONFIG' % project.upper()] = ''
# http://code.google.com/p/modwsgi/wiki/ApplicationIssues#User_HOME_Environment_Variable
# os.environ['HOME'] = pwd.getpwuid(os.getuid()).pw_dir

# activate virtualenv
# activate_this = os.path.join(BASE_DIR, "env/bin/activate_this.py")
# execfile(activate_this, dict(__file__=activate_this))

BASE_DIR = os.path.join(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import the config for the proper environment using the shell var APP_ENV
env = os.environ.get('APP_ENV', 'development')

# give wsgi the "application"
application = create_app('app.config.settings.{0}Config'.format(env.capitalize()), env=env)
CORS(application, resources={r"/v1/*": {"origins": "*", "supports_credentials": True}})
