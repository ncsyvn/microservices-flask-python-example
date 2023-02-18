import json
from datetime import timedelta

from flask import Blueprint, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt, jwt_refresh_token_required)
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.helper import get_permissions
from app.api.helper import send_error, send_result
from app.enums import FORGOT_PASSWORD_VALID_OTP, REGISTER_STEP_3, INVALID_PARAMETERS_ERROR
from app.extensions import jwt, db
from app.gateway import authorization_require
from app.models import Token, User
from app.utils import logged_input, get_timestamp_now, is_contain_space, get_another_phone
from app.validator import AuthValidation, SendOTPValidation, RegisterCheckOPTSchema, \
    UserSchema, PasswordInitializationSchema

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


@api.route('/login', methods=['POST'])
def login():
    """
    This is controller of the login api

    Requests Body:
            email: string, require

            password: string, require
            phone: string, optional
            otp: string,optional

    Returns:
            {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username
            }

    Examples::
        {
            "code": 200,
            "data": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjU3Mjg1MTQsIm5iZiI6MTYyNTcyODUxNCwianRpIjoiODkzNDYwMjMtZTkyOS00YmM2LWIyMDktZWVlYzI2Yzg0OTA2IiwiZXhwIjoxNjI2NTkyNTE0LCJpZGVudGl0eSI6ImFkbWluIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.qBSx-4u22a3zG2eJUKGhd714swX4zmLJ5WGCpQLzLQM",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjU3Mjg1MTQsIm5iZiI6MTYyNTcyODUxNCwianRpIjoiMGVhNWEzMzAtZmZhYi00Mzk3LTgzOWQtYzQ2Y2VlYjIzY2RkIiwiZXhwIjoxNjI3NDU2NTE0LCJpZGVudGl0eSI6ImFkbWluIiwidHlwZSI6InJlZnJlc2gifQ.qlM2GGju3k9d9J05t4qNu9iM_uqUdmf7DHB2MW1Tb24",
                "email": "admin"
            },
            "jsonrpc": "2.0",
            "message": "Logged in successfully!",
            "status": true,
            "version": "Mayno website v1.0"
        }

    """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        json_body.setdefault(key, str(value).strip())

    # validate request body
    validator_input = AuthValidation()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id=INVALID_PARAMETERS_ERROR)

    # Check username and password
    email = json_body.get("email")
    phone = json_body.get("phone")
    password = json_body.get("password")
    otp = json_body.get("otp")

    if email:
        # Admin user can't login to user side and normal user can't login to admin side
        user = User.query.filter(User.email == email, User.type != 1).first()
        if user is None or (password and not check_password_hash(user.password_hash, password)):
            return send_error(message_id=INCORRECT_EMAIL_PASSWORD)
    else:
        another_phone = get_another_phone(phone)
        user = User.query.filter(or_(User.phone == phone, User.phone == another_phone),
                                 User.register_status >= REGISTER_STEP_3, User.type == 1).first()
        if user is None or (password and not check_password_hash(user.password_hash, password)):
            return send_error(message_id=WRONG_PHONE_PASSWORD)

    if not user.is_active:
        return send_error(message_id=INACTIVE_ACCOUNT_ERROR)

    if otp and str(user.otp) != otp:
        return send_error(message_id=WRONG_OTP)
    if otp and user.otp_ttl < get_timestamp_now():
        return send_error(message_id=OTP_EXPIRED)

    list_permission = get_permissions(user)
    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES,
                                       user_claims={"list_permission": list_permission,
                                                    "force_change_password": user.force_change_password})
    refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES,
                                         user_claims={"list_permission": list_permission,
                                                      "force_change_password": user.force_change_password})

    # Store the tokens in our store with a status of not currently revoked.
    Token.add_token_to_database(access_token, user.id)
    Token.add_token_to_database(refresh_token, user.id)

    data: dict = UserSchema().dump(user)
    data.setdefault('access_token', access_token)
    data.setdefault('refresh_token', refresh_token)

    return send_result(data=data, message="Logged in successfully!")


@api.route('/send_otp', methods=['POST'])
def send_otp():
    """
    This is controller of the send otp api

    Requests Body:
            phone: string, require

    Returns:
            {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username
            }

    Examples::
        {
            "code": 200,
            "data": {},
            "message": "Send OTP successfully!",
            "status": true,
            "version": "Mayno website v1.0"
        }

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
        json_body.setdefault(key, str(value).strip())

    # validate request body
    validator_input = SendOTPValidation()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id=INVALID_PARAMETERS_ERROR)

    # Check username and password
    phone = json_body.get("phone")
    another_phone = get_another_phone(phone)
    user = User.query.filter(or_(User.phone == phone, User.phone == another_phone),
                             User.register_status >= REGISTER_STEP_3, User.is_active == True).first()
    if user is None:
        return send_error(message_id=PHONE_DOES_NOT_EXISTS)

    # TODO: generate OTP code and send to user phone number
    # Default OTP 123456 and TTL = 5 minute
    user.otp = 123456
    user.otp_ttl = get_timestamp_now() + 60 * 5
    db.session.commit()

    data = {
        "user_id": user.id
    }

    return send_result(message_id=NEW_OTP_SENT, data=data)


@api.route('/check_otp', methods=['POST'])
def check_otp():
    """
    This api reset check OTP

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
        json_body.setdefault(key, str(value).strip())

    # validate request body
    validator_input = RegisterCheckOPTSchema()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id=INVALID_PARAMETERS_ERROR)

    otp = json_body.get("otp")
    user_id = json_body.get("user_id")
    user = User.query.get(user_id)
    if user is None:
        return send_error(message_id=PHONE_DOES_NOT_EXISTS)

    if user.otp_ttl < get_timestamp_now():
        return send_error(message_id=OTP_EXPIRED)

    if otp != user.otp:
        return send_error(message_id=WRONG_OTP)

    user.register_status = FORGOT_PASSWORD_VALID_OTP
    db.session.commit()

    return send_result(data=UserSchema().dump(user), message="Check otp successfully!")


@api.route('/reset_password', methods=['POST'])
def reset_password():
    """
    This api reset password current user, revoke all access token of current user

    Examples::

    """
    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message="Request Body incorrect json format: " + str(ex), code=442)

    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        json_body.setdefault(key, str(value).strip())

    # validate request body
    validator_input = PasswordInitializationSchema()
    is_not_validate = validator_input.validate(json_body)
    if is_not_validate:
        return send_error(data=is_not_validate, message_id=INVALID_PARAMETERS_ERROR)

    password = json_body.get("password")
    if is_contain_space(password):
        return send_error(message='Password cannot contain spaces')

    user_id = json_body.get("user_id")
    user = User.query.filter_by(id=user_id, register_status=FORGOT_PASSWORD_VALID_OTP).first()

    if user is None:
        return send_error(message_id=PHONE_DOES_NOT_EXISTS)
    user.password_hash = generate_password_hash(password)
    user.register_status = REGISTER_STEP_3
    user.modified_date_password = get_timestamp_now()
    db.session.commit()

    # revoke all token of current user  from database except current token
    Token.revoke_all_token(get_jwt_identity())

    # Process to this user login new session
    list_permission = get_permissions(user)
    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES,
                                       user_claims={"list_permission": list_permission,
                                                    "force_change_password": user.force_change_password})
    refresh_token = create_refresh_token(identity=user.id, expires_delta=REFRESH_EXPIRES,
                                         user_claims={"list_permission": list_permission,
                                                      "force_change_password": user.force_change_password})

    # Store the tokens in our store with a status of not currently revoked.
    Token.add_token_to_database(access_token, user.id)
    Token.add_token_to_database(refresh_token, user.id)

    data: dict = UserSchema().dump(user)
    data.setdefault('access_token', access_token)
    data.setdefault('refresh_token', refresh_token)

    return send_result(data=data, message="Bạn đã đổi mật khẩu thành công")


@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    This api use for refresh expire time of the access token. Please inject the refresh token in Authorization header

    Requests Body:

        refresh_token: string,require
        The refresh token return in the login API

    Returns:

        access_token: string
        A new access_token

    Examples::

    """

    user_identity = get_jwt_identity()
    user = User.get_by_id(user_identity)

    list_permission = get_permissions(user)
    access_token = create_access_token(identity=user.id, expires_delta=ACCESS_EXPIRES,
                                       user_claims={"list_permission": list_permission,
                                                    "force_change_password": user.force_change_password})

    # Store the tokens in our store with a status of not currently revoked.
    Token.add_token_to_database(access_token, user_identity)

    data = {
        'access_token': access_token
    }

    return send_result(data=data)


@api.route('/logout', methods=['DELETE'])
@authorization_require()
def logout():
    """
    This api logout current user, revoke current access token

    Examples::

    """

    jti = get_raw_jwt()['jti']
    Token.revoke_token(jti)  # revoke current token from database

    return send_result(message="Logout successfully!")


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    """
    :param decrypted_token:
    :return:
    """
    return Token.is_token_revoked(decrypted_token)


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return send_error(code=401, message_id=SESSION_EXPIRED)


@jwt.revoked_token_loader
def revoked_token_callback():
    return send_error(code=401, message_id=SESSION_EXPIRED)
