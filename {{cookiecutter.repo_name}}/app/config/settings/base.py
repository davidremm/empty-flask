import os


class BaseConfig(object):
    APP_ROOT = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            os.pardir, os.pardir
        )
    )
    PROJECT_ROOT = os.path.realpath(os.path.join(APP_ROOT, os.pardir))
    LOG_PATH = os.path.join(PROJECT_ROOT, 'logs')
