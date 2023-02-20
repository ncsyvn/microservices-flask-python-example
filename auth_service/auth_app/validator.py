from marshmallow import Schema, fields, validate
from auth_app.utils import REGEX_EMAIL, REGEX_VALID_PASSWORD


class LoginBodyValidation(Schema):
    """
    Validate body of login api
    :param
        email: string, required
        password: string, required
    Ex:
    {
        "email": "sy123456@gmail.com",
        "password": "123456aA@"
    }
    """
    email = fields.String(required=True, validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_EMAIL)])
    password = fields.String(required=True,
                             validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])


class SignupBodyValidation(Schema):
    """
    Validate body of signup api
    :param
        email: string, required
        password: string, required
    Ex:
    {
        "email": "sy123456@gmail.com",
        "password": "12345678aA@"
    }
    """
    email = fields.String(required=True, validate=[validate.Length(min=1, max=50), validate.Regexp(REGEX_EMAIL)])
    password = fields.String(required=True,
                             validate=[validate.Length(min=1, max=16), validate.Regexp(REGEX_VALID_PASSWORD)])


class UserSchema(Schema):
    """
    User Schema

    """
    id = fields.String()
    email = fields.String()
    phone = fields.String()
    address = fields.String()
    created_date = fields.Number()
    modified_date = fields.Number()
    is_active = fields.Boolean()
