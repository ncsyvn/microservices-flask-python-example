import json
import uuid
from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt, jwt_refresh_token_required)
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash
from auth_app.api.helper import send_error, send_result
from auth_app.utils import logged_input, get_timestamp_now
from auth_app.validator import SignupUserSchema
from auth_app.models import User
from auth_app.extensions import db

ACCESS_EXPIRES = timedelta(days=1)
REFRESH_EXPIRES = timedelta(days=5)
api = Blueprint('auth', __name__)

# Message_ID variable
NEW_OTP_SENT = '301'
WRONG_OTP = '305'
OTP_EXPIRED = '306'
PHONE_DOES_NOT_EXISTS = '307'
WRONG_PHONE_PASSWORD = '308'
INCORRECT_EMAIL_PASSWORD = "396"
INACTIVE_ACCOUNT_ERROR = "414"
SESSION_EXPIRED = '343'


@api.route('/signup', methods=['POST'])
def signup():
    """ This is api for the user signup function.

        Request Body:

        Returns:

        Examples::
    """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    logged_input(json.dumps(json_req))
    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        if isinstance(value, str):
            json_body.setdefault(key, value.strip())
        else:
            json_body.setdefault(key, value)

    # validate request body
    validator_input = SignupUserSchema()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message="Invalid parameters")

    email = json_body.get("email")
    password = json_body.get("password")
    duplicated_user = User.query.filter(User.email == email).first()
    if duplicated_user:
        return send_error(message="User existed")

    created_date = get_timestamp_now()
    _id = str(uuid.uuid4())
    password_hash = generate_password_hash(password)
    new_user = User(id=_id, email=email, password_hash=password_hash, created_date=created_date)
    db.session.add(new_user)
    db.session.commit()

    data = {
        "user_id": _id
    }

    return send_result(data=data)
