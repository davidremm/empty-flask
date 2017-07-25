from flask import g


class Couchdb(object):
    def __init__(self, dbms):
        self.app        = None
        self.dbms       = dbms
        self.connection = None

    def init_app(self, app):
        self.app = app
        self.app.before_request(self.connect)
        self.app.teardown_appcontext(self._teardown_appcontext)

    def connect(self):
        if self.dbms is 'couchdb':
            import couchdb
            connection = couchdb.Server(self.app.config['COUCHDB_HOST'])

            if 'COUCHDB_USER' in self.app.config and 'COUCHDB_PASSWORD' in self.app.config:
                connection.resource.credentials = (self.app.config['COUCHDB_USER'], self.app.config['COUCHDB_PASSWORD'])

            g.couchdb = connection

        else:
            raise AttributeError('Wasn\'t able to find couchdb in dbms.')

    def _configure_credentials(self, user, password):
        # TODO: add support for sql alch
        connection = self.connection

        if connection is not None:
            connection.resource.credentials = (user, password)

    def _teardown_appcontext(self, exception):
        self._disconnect()

    def _disconnect(self):
        connection = getattr(g, self.dbms, None)
        if connection is not None:
            del connection
