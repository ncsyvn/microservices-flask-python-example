import requests
from functools import wraps
from flask import request
from video_app.enums import VALIDATE_TOKEN_URL
from video_app.utils import logged_error
from video_app.api.helper import send_error


def authorization_require():
    """
    Validate token by auth_service
    Args:

    Returns:

    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            authorization = request.headers.get('Authorization', '').strip()
            try:
                res = requests.get(VALIDATE_TOKEN_URL, headers={"Authorization": authorization}).json()
            except Exception as ex:
                logged_error(f"Call validate token api failed: {ex}")
                return send_error(message="You don't have permission")
            if 'message' in res and res['message']['status'] == 'success':
                return fn(*args, **kwargs)
            else:
                return send_error(message="You don't have permission")
        return decorator
    return wrapper