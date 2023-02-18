from functools import wraps

from flask import request
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)

from auth_app.api.helper import send_error


def authorization_require():
    """
    validate authorization follow permission user
    Args:

    Returns:

    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            permission_route = "{0}@{1}".format(request.method.lower(), request.url_rule.rule)
            claims = get_jwt_claims()

            if claims.get("force_change_password"):
                return send_error(message='You have to change your password before do this action')

            list_permission = claims.get("list_permission")
            if permission_route in list_permission:
                return fn(*args, **kwargs)
            else:
                return send_error(message='You do not have permission')

        return decorator

    return wrapper
