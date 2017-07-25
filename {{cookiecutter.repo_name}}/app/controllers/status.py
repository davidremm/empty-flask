from datetime        import datetime
from flask           import Blueprint

from app.api_response import ApiResponse

status = Blueprint('status', __name__)


@status.route('/status', methods=["GET"])
def display_status():
    """
    Provides status of app and dependencies.
    """
    response = ApiResponse('status')

    response.resource_data = {
        "service_name": "flask-boilerplate",
        "build_date": datetime.utcnow(),
        "version": "1.0.0",
        "SHA": "github sha"
    }

    response.status_code = 200

    return response.serialize('json')
