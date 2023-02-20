import datetime
import json
import random
import string
from abc import ABC
from html.parser import HTMLParser
from time import strftime

from flask import request
from pytz import timezone
from .extensions import logger
from auth_app.enums import TIME_FORMAT_LOG


def logged_error(error: str) -> None:
    """
    Logged error
    :param error:
    :return:
    """

    logger.info('%s %s %s %s %s ERROR: %s',
                strftime(TIME_FORMAT_LOG),
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                error)


def logged_input(json_req: str) -> None:
    """
    Logged input fields
    :param json_req:
    :return:
    """

    logger.info('%s %s %s %s %s INPUT FIELDS: %s',
                strftime(TIME_FORMAT_LOG),
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                json_req)


def get_timestamp_now() -> int:
    """
        Returns:
            current time in timestamp
    """
    time_zon_sg = timezone('Asia/Ho_Chi_Minh')
    return int(datetime.datetime.now(time_zon_sg).timestamp())


# Regex validate
REGEX_EMAIL = r'^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,' \
              r';:\s@\"]{2,})$'
REGEX_VALID_PASSWORD = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?!.* ).{8,16}$'
