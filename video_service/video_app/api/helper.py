import os
from flask import jsonify
from video_app.settings import ProdConfig, StgConfig

CONFIG = ProdConfig if os.environ.get('ENV') == 'prd' else StgConfig


def send_result(data: any = None, message: str = "OK", code: int = 200,
                status: str = 'success', show: bool = False, duration: int = 0):
    """
    Args:
    :param data: whatever you want
    :param message: error message
    :param code: 200 is success
    :param status: error
    :param show: show popup or not (useful for Frontend team)
    :param duration: show popup for duration second
    :return:
    """
    message_dict = {
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


def send_error(data: any = None, message: str = "Error", code: int = 200,
               status: str = 'error', show: bool = False, duration: int = 0):
    """
    Args:
    :param data: whatever you want
    :param message: error message
    :param code: you can use 4xx
    :param status: error
    :param show: show popup or not (useful for Frontend team)
    :param duration: show popup for duration second
    :return:
    """
    message_dict = {
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


