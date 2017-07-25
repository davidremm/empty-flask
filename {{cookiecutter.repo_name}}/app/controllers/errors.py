from flask          import Blueprint, g
from werkzeug.local import LocalProxy

from app.api_response import ApiResponse

notifications = LocalProxy(lambda: g.notifications)
errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    response = ApiResponse('not_found')
    notifications['errors'] = {'type': 'not_found', 'details': 'Route not found.'}

    return response.serialize('json')
