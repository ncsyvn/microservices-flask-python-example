import os
from flask import jsonify
from auth_app.settings import ProdConfig, StgConfig
# call config service

CONFIG = ProdConfig if os.environ.get('ENV') == 'prd' else StgConfig


def send_result(data: any = None, message_id: str = '', message: str = "OK", code: int = 200,
                status: str = 'success', show: bool = False, duration: int = 0):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
        version: version of api
    :param data:
    :param message_id:
    :param message:
    :param code:
    :param status:
    :param show:
    :param duration:
    :return:
    json rendered sting result
    """
    message_dict = {
        "id": message_id,
        "text": message,
        "status": status,
        "show": show,
        "duration": duration,
    }
    res = {
        "code": code,
        "data": data,
        "message": message_dict,
    }

    return jsonify(res), 200


def send_error(data: any = None, message_id: str = '', message: str = "Error", code: int = 200,
               status: str = 'error', show: bool = False, duration: int = 0):
    """

    :param data:
    :param message_id:
    :param message:
    :param code:
    :param status:
    :param show:
    :param duration:
    :return:
    """
    message_dict = {
        "id": message_id,
        "text": message,
        "status": status,
        "show": show,
        "duration": duration,
    }
    res = {
        "code": code,
        "data": data,
        "message": message_dict,
    }

    return jsonify(res), code


