# coding: utf-8
from sqlalchemy.dialects.mysql import INTEGER
from video_app.extensions import db
from video_app.utils import get_timestamp_now


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(500), primary_key=True)
    url = db.Column(db.String(1000))
    thumbnail_url = db.Column(db.String(1000))
    created_date = db.Column(INTEGER(unsigned=True), default=get_timestamp_now(), index=True)
    modified_date = db.Column(INTEGER(unsigned=True), default=0)
    is_deleted = db.Column(db.Boolean, default=0)
    is_active = db.Column(db.Boolean, default=1)
