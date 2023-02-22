from functools import wraps
from flask import request
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
            access_token = request.headers.get('access_token', '')
        return decorator
    return wrapper
