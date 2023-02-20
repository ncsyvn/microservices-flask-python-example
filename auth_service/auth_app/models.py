# coding: utf-8
import uuid
from flask_jwt_extended import decode_token, get_jwt_identity, get_raw_jwt
from sqlalchemy.dialects.mysql import INTEGER
from auth_app.extensions import db
from auth_app.utils import get_timestamp_now


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    created_date = db.Column(INTEGER(unsigned=True), default=get_timestamp_now(), index=True)
    modified_date = db.Column(INTEGER(unsigned=True), default=0)
    is_deleted = db.Column(db.Boolean, default=0)
    is_active = db.Column(db.Boolean, default=1)

    def get_password_age(self):
        return int((get_timestamp_now() - self.modified_date_password) / 86400)

    @classmethod
    def get_current_user(cls):
        return cls.query.get(get_jwt_identity())

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.String(50), primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(INTEGER(unsigned=True), nullable=False)

    @staticmethod
    def add_token_to_database(encoded_token, user_identity):
        """
        Adds a new token to the database. It is not revoked when it is added.
        :param encoded_token:
        :param user_identity:
        """
        decoded_token = decode_token(encoded_token)
        jti = decoded_token['jti']
        token_type = decoded_token['type']
        expires = decoded_token['exp']
        revoked = False
        _id = str(uuid.uuid4())

        db_token = Token(
            id=_id,
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            expires=expires,
            revoked=revoked,
        )
        db.session.add(db_token)
        db.session.commit()

    @staticmethod
    def prune_database():
        """
        Delete tokens that have expired from the database.
        How (and if) you call this is entirely up you. You could expose it to an
        endpoint that only administrators could call, you could run it as a cron,
        set it up with flask cli, etc.
        """
        now_in_seconds = get_timestamp_now()
        Token.query.filter(Token.expires < now_in_seconds).delete()
        db.session.commit()
