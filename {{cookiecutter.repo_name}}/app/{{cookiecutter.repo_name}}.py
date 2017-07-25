import os

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

# import assets and notifications
from app.config               import assets
from app.config.notifications import Notifications

# import extensions
from app.config.extensions import (
    cache,
    assets_env,
    debug_toolbar
)


def create_app(object_name, env="development"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    :argument string object_name: Object name
    :argument string env: Environment
    """
    app = Flask(__name__)
    app.config.from_object(object_name)
    app.config['ENV'] = env

    configure_logging(app)

    # init the cache
    cache.init_app(app)

    # init debug toolbar
    debug_toolbar.init_app(app)

    # init notifications object
    notifications = Notifications()
    notifications.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register index blueprint
    from app.controllers.index import index
    app.register_blueprint(index)

    # register api blueprints
    api_prefix = "/{0}".format(app.config['API_VERSION'])

    from app.controllers.errors import errors
    app.register_blueprint(errors, url_prefix=api_prefix)

    from app.controllers.status import status
    app.register_blueprint(status, url_prefix=api_prefix)

    return app


def configure_logging(app):
    """
    """
    import logging
    import logging.config
    import json

    if not os.path.exists(app.config["LOG_PATH"]):
        os.mkdir(app.config["LOG_PATH"])

    with open(os.path.join(app.config['APP_ROOT'], 'config/logging.json')) as file:
        logging_config = json.load(file)

        if 'handlers' in logging_config:
            for handler in logging_config['handlers'].values():
                    if 'File' in handler['class']:
                        handler['filename'] = os.path.join(app.config['LOG_PATH'], handler['filename'])

        if app.config['ENV'].lower() in ('staging', 'development', 'test'):
            logging_config["root"]["handlers"] = ["console"]

        logging.config.dictConfig(logging_config)

    app.logger.info("Logging has been configured for {}".format(app.config['ENV'].lower()))
