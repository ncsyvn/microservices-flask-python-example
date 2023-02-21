from marshmallow import Schema, fields, validate


class CreateVideoSchema(Schema):
    """
    Validate body of create video api
    :param
        title: string, required
        url: string, optional
        thumbnail_url: string, optional
    Ex:
    {
        "title": "This is the first video",
        "url": "https://video.com/123",
        "thumbnail_url": "https://thumbnail.com/123"
    }
    """
    title = fields.String(required=True, validate=[validate.Length(min=1, max=500)])
    url = fields.String(required=False, validate=[validate.Length(min=1, max=1000)])
    thumbnail_url = fields.String(required=False, validate=[validate.Length(min=1, max=1000)])


class VideoSchema(Schema):
    """
    Video Schema

    """
    id = fields.String()
    title = fields.String()
    url = fields.String()
    thumbnail_url = fields.String()
    created_date = fields.Number()
    modified_date = fields.Number()
    is_deleted = fields.Boolean()
    is_active = fields.Boolean()
