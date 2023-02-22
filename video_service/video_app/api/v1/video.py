import json
import uuid

from flask import Blueprint, request
from video_app.utils import logged_input, get_timestamp_now
from video_app.validator import CreateVideoSchema, VideoSchema
from video_app.models import Video
from video_app.api.helper import send_error, send_result
from video_app.extensions import db
from video_app.gateway import authorization_require

api = Blueprint('videos', __name__)


@api.route('', methods=['GET'])
def search_videos():
    """
    Search video api
    Requests params:
            keyword: string, optional
    Returns:
            list videos
    """

    keyword = request.args.get('keyword', '').strip()
    videos = Video.query.filter(Video.title.ilike(f'%{keyword}%')).all()
    videos_dumped = VideoSchema(many=True).dumps(videos)
    return send_result(data=json.loads(videos_dumped))


@api.route('', methods=['POST'])
@authorization_require()
def create_new_video():
    """
    Create new video API.
    Requests Body:
            title: string, require
            url: string, optional
            thumbnail_url: string, optional
    Returns:
            id of new video
    """

    try:
        json_req = request.get_json()
    except Exception as ex:
        return send_error(message='Request Body incorrect json format: ' + str(ex), code=442)

    logged_input(json.dumps(json_req))
    if json_req is None:
        return send_error(message='Please check your json requests', code=442)

    # trim input body
    json_body = {}
    for key, value in json_req.items():
        json_body.setdefault(key, str(value).strip())

    # validate request body
    is_not_validate = CreateVideoSchema().validate(json_body)  # Dictionary show detail error fields
    if is_not_validate:
        return send_error(data=is_not_validate, message='Invalid params')

    title = json_body.get('title')
    url = json_body.get('url', '')
    thumbnail_url = json_body.get('thumbnail_url', '')
    _id = str(uuid.uuid4())
    # Store video to db
    new_video = Video(id=_id, title=title, url=url, thumbnail_url=thumbnail_url)
    db.session.add(new_video)
    db.session.commit()
    data = {
        'video_id': _id
    }
    return send_result(data)
