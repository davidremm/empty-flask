from flask import g
from collections import UserDict


class Notifications(object):
    """Create a notifications object to allow for user warnings and errors.
    """
    def __init__(self):
        self.app = None

    def init_app(self, app):
        """ Create connection for Application to to process the request
        :param app: Application Connection created
        :return: None
        """
        self.app = app
        self.app.before_request(self._create_notifications_obj)
        # self.app.after_request(self._destroy_notifications_)

    def _create_notifications_obj(self):
        """Verify dbms type and based off type follow logic
        :rtype: object: return connection to Flask Application
        """
        g.notifications = NotificationsDict()

    def _teardown_appcontext(self, exception):
        """ Disconnection connection to RDBMS
        :param exception:
        :return: connection
        """


class NotificationsDict(UserDict):
    """
    """
    def __init__(self):
        UserDict.__init__(self)
        self.data['errors']   = []
        self.data['warnings'] = []
        self.data['info']     = []

    def __dict__(self):
        notifications = {}

        for key in ('errors', 'warnings', 'info'):
            if self.data.get(key, False):
                notifications[key] = self.data[key]

        return notifications

    def __setitem__(self, key, notification):
        if not isinstance(notification, dict):
            raise KeyError("notification must be a dict")

        for field in ('details', 'type'):
            if field not in notification:
                raise KeyError("{0} must be present.".format(field))

        if key not in self.data:
            raise IndexError("The only supported Notifications are {*}".format(",".join(self.data.keys())))

        self.data[key].append(notification)

    def empty(self):
        self.data['errors']   = []
        self.data['warnings'] = []
        self.data['info']     = []
