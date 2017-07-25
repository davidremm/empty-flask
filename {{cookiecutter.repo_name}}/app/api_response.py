from datetime       import datetime

from flask          import Response
from flask          import json, g
from werkzeug.local import LocalProxy

notifications = LocalProxy(lambda: g.notifications)

ERRORS = {
    "unauthorized": {
        "status_code": 401,
        "details": "Not authorized."
    },
    "malformed": {
        "status_code": 400,
        "details": "malformed body."
    },
    "bad_request": {
        "status_code": 400,
        "details": "Any case where a parameter is invalid, or a required parameter is missing."
    },
    "forbidden": {
        "status_code": 403,
        "details": "The requested information cannot be viewed."},

    "not_found": {
        "status_code": 404,
        "details": "Document was not found."
    },
    "method_not_found": {
        "status_code": 405,
        "details": "couldn't find the requested endpoint."
    },
    "conflict": {
        "status_code": 409,
        "details": "Document already exists."
    },
    "param_error": {
        "status_code": 400,
        "details": "missing a parameter."
    },
    "internal_server_error": {
        "status_code": 500,
        "details": "The server encountered an unexpected condition which prevented it from fulfilling the request."
    }
}


class ApiResponse(Response):

    def __init__(self, resource, resource_data={}, headers=None, status=None, mimetype='application/json', **kwargs):
        self._metadata      = MetaData()
        self._notifications = notifications
        self._resource      = resource
        self._response_body = {
            self._resource: resource_data,
            'metadata': self._metadata,
            'notifications': self._notifications
        }

        super().__init__(
            "call response.serialize(format) to return api response.",
            headers=headers,
            status=status,
            mimetype=mimetype,
            direct_passthrough=True,
            **kwargs
        )

    def serialize(self, format):
        if not isinstance(format, str) or format not in ('json',):
            raise TypeError("We are only allowing users to serialize their data to json formats.")

        if self._notifications.get('errors'):
            # set default error status code if someone sends one off error.
            self.status_code = 400

            for error in self._notifications['errors']:
                defined_error = ERRORS.get(error['type'].lower())

                if defined_error:
                    self.status_code = defined_error['status_code']

        # TODO: support xml
        self.mimetype = 'application/json'
        self.data     = json.dumps(self._response_body, cls=ObjectEncoder)

        return self

    @property
    def status_code(self):
        return Response.status_code.fget(self)

    @status_code.setter
    def status_code(self, status_code):
        Response.status_code.fset(self, status_code)
        self._metadata.status_code = self.status_code

    @property
    def notifications(self):
        return self._notifications

    @property
    def meta_data(self):
        return self._metadata

    @property
    def resource(self):
        return self._resource

    @property
    def resource_data(self):
        return self._response_body[self._resource]

    @resource_data.setter
    def resource_data(self, value):
        self._response_body[self._resource] = value


class MetaData(object):
    def __init__(self, **kwargs):
        self._limit          = None
        self._off_set        = None
        self._request_time   = None
        self._status_code    = None
        self._total_results  = None
        self._query          = None

    def __dict__(self):
        return dict([(name, getattr(self, name)) for name in dir(self)
                     if getattr(self, name) and not name.startswith('_') and not callable(getattr(self, name))])

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value):
        self._limit = value

    @property
    def off_set(self):
        return self._off_set

    @off_set.setter
    def off_set(self, value):
        self._off_set = value

    @property
    def request_time(self):
        return self._request_time

    @request_time.setter
    def request_time(self, value):
        self._request_time = value

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value):
        self._status_code = value

    @property
    def total_results(self):
        return self._total_results

    @total_results.setter
    def total_results(self, value):
        self._total_results = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value


class ObjectEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')

        if hasattr(o, '__dict__'):
            if callable(o.__dict__):
                return o.__dict__()
            else:
                return o.__dict__

        return o
