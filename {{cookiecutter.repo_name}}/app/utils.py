import re

from flask           import request, g
from flask.ext.login import current_user as ext_current_user, login_user
from werkzeug.local  import LocalProxy

notifications = LocalProxy(lambda: g.notifications)
current_user  = LocalProxy(lambda: get_current_user())

# pre-compile regex
# there is a small bug in this where if you pass SomethingIs_Okay you will get two _ between is and okay
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def normalize_keys(suspect):
    """
    take a dict and turn all of its type string keys into snake_case
    """
    if type(suspect) is not dict:
        raise TypeError('you must pass a dict.')

    for key in suspect.keys():
        if not isinstance(key, str):
            continue

        s1 = first_cap_re.sub(r'\1_\2', key)
        new_key = all_cap_re.sub(r'\1_\2', s1).lower()

        value = suspect.pop(key)
        if type(value) is dict:
            suspect[new_key] = normalize_keys(value)
        elif type(value) is list:
            suspect[new_key] = [normalize_keys(x) if type(x) is dict else x for x in value]
        else:
            suspect[new_key] = value

    return suspect


def valid_uri(uri):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', flags=re.IGNORECASE)

    if regex.match(uri):
        return True
    else:
        return False


def get_current_user():
    """
    Get current user check it see if user is anonymous if so check if oauth in request. if so log oauth user in.
    """
    if ext_current_user.is_anonymous():
        if hasattr(request, 'oauth'):
            login_user(user=request.oauth.user)

    return ext_current_user
