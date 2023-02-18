import datetime
import json
import random
import string
from abc import ABC
from html.parser import HTMLParser
from time import strftime

from flask import request
from marshmallow import fields, validate as validate_
from pytz import timezone
from .extensions import logger
import re


class FieldString(fields.String):
    """
    validate string field, max length = 1024
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, requirement=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        if requirement is not None:
            validate = validate_.NoneOf(error='Invalid input!', iterable={'full_name'})
        super(FieldString, self).__init__(validate=validate, required=requirement, **metadata)


class FieldNumber(fields.Number):
    """
    validate number field, max length = 30
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)


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


def logged_error(error: str) -> None:
    """
    Logged input fields
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


def allowed_file(filename: str) -> bool:
    """

    Args:
        filename:

    Returns:

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FILES


def get_datetime_now() -> datetime:
    """
        Returns:
            current datetime
    """
    time_zon_sg = timezone('Asia/Ho_Chi_Minh')
    return datetime.datetime.now(time_zon_sg)


def get_timestamp_now() -> int:
    """
        Returns:
            current time in timestamp
    """
    time_zon_sg = timezone('Asia/Ho_Chi_Minh')
    return int(datetime.datetime.now(time_zon_sg).timestamp())


def get_timestamp_begin_today() -> int:
    """
        Returns:
            current time in timestamp
    """
    return get_timestamp_now() - get_timestamp_now() % 86400 - 7 * 3600


def is_contain_space(password: str) -> bool:
    """

    Args:
        password:

    Returns:
        True if password contain space
        False if password not contain space

    """
    return ' ' in password


def allowed_file_img(filename):
    """

    Args:
        filename:

    Returns:

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMG


def get_another_phone(phone: str):
    """

    Args:
        phone:

    Returns:

    """
    if phone[0] == '+':
        return '0' + phone[3:]
    return '+84' + phone[1:]


def are_equal(arr1: list, arr2: list) -> bool:
    """
    Check two array are equal or not
    :param arr1: [int]
    :param arr2: [int]
    :return:
    """
    if len(arr1) != len(arr2):
        return False

    # Sort both arrays
    arr1.sort()
    arr2.sort()

    # Linearly compare elements
    for i, j in zip(arr1, arr2):
        if i != j:
            return False

    # If all elements were same.
    return True


def generate_password():
    """
    :return: random password
    """
    symbol_list = ["@", "$", "!", "%", "*", "?", "&"]
    number = '0123456789'
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choices(letters_and_digits, k=6))
    return '{}{}{}'.format(result_str, random.choice(symbol_list), random.choice(number))


def decode_redis_message(redis_byte_obj):
    """

    :param redis_byte_obj:
    :return:
    """
    return_data = json.loads(redis_byte_obj.decode()) if type(redis_byte_obj) == bytes else None
    return return_data


def escape_wildcard(search):
    """
    :param search:
    :return:
    """
    search1 = str.replace(search, '\\', r'\\')
    search2 = str.replace(search1, r'%', r'\%')
    search3 = str.replace(search2, r'_', r'\_')
    search4 = str.replace(search3, r'[', r'\[')
    search5 = str.replace(search4, r'"', r'\"')
    search6 = str.replace(search5, r"'", r"\'")
    return search6


def no_accent_vietnamese(s):
    """
        Function convert string vietnamese
        Returns: string not mark
        Examples::
    """
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s


def is_contained_accent_vietnamese(s: str) -> bool:
    """

    :param s:
    :return:
    """
    accent_vietnamese = ['à', 'á', 'ạ', 'ả', 'ã', 'â', 'ầ', 'ấ', 'ậ', 'ẩ', 'ẫ', 'ă', 'ằ', 'ắ', 'ặ', 'ẳ', 'ẵ', 'À', 'Á',
                         'Ạ', 'Ả', 'Ã', 'Ă', 'Ằ', 'Ắ', 'Ặ', 'Ẳ', 'Ẵ', 'Â', 'Ầ', 'Ấ', 'Ậ', 'Ẩ', 'Ẫ', 'è', 'é', 'ẹ', 'ẻ',
                         'ẽ', 'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ', 'È', 'É', 'Ẹ', 'Ẻ', 'Ẽ', 'Ê', 'Ề', 'Ế', 'Ệ', 'Ể', 'Ễ', 'ò',
                         'ó', 'ọ', 'ỏ', 'õ', 'ô', 'ồ', 'ố', 'ộ', 'ổ', 'ỗ', 'ơ', 'ờ', 'ớ', 'ợ', 'ở', 'ỡ', 'Ò', 'Ó', 'Ọ',
                         'Ỏ', 'Õ', 'Ô', 'Ồ', 'Ố', 'Ộ', 'Ổ', 'Ỗ', 'Ơ', 'Ờ', 'Ớ', 'Ợ', 'Ở', 'Ỡ', 'ì', 'í', 'ị', 'ỉ', 'ĩ',
                         'Ì', 'Í', 'Ị', 'Ỉ', 'Ĩ', 'ù', 'ú', 'ụ', 'ủ', 'ũ', 'ư', 'ừ', 'ứ', 'ự', 'ử', 'ữ', 'Ư', 'Ừ', 'Ứ',
                         'Ự', 'Ử', 'Ữ', 'Ù', 'Ú', 'Ụ', 'Ủ', 'Ũ', 'ỳ', 'ý', 'ỵ', 'ỷ', 'ỹ', 'Ỳ', 'Ý', 'Ỵ', 'Ỷ', 'Ỹ', 'Đ',
                         'đ']
    for accent in accent_vietnamese:
        if accent in s:
            return True
    return False


def convert_link_seo(s):
    """
        Function convert string vietnamese
        Returns: link seo
        Examples::
    """
    link_seo = no_accent_vietnamese(s)
    link_seo = link_seo.lower()
    link_seo = link_seo.replace(" ", "-")
    link_seo = re.sub('[^A-Za-z0-9 -]+', '', link_seo)
    return link_seo


def check_format_email(email):
    """
    :param email:
    :return:
    False if email format  incorrect else true
    """
    # pass the regular expression
    # and the string in search() method
    regex = r"^[A-Z0-9a-z_.%+-]+[@]\w+[A-Za-z0-9.-]\w{2,}"
    return re.search(regex, email)


def check_format_phone(phone):
    """
    :param phone:
    :return:
    False if phone format  incorrect else true
    """
    # pass the regular expression
    # and the string in search() method
    # regex = r'(84|0[3|5|7|8|9])+([0-9]{8})\b'
    # regex = r'(84|0[1-9])+([0-9]{8})\b'
    regex = r'^\+?[0-9]{0,20}$'
    return re.search(regex, phone)


class CustomHTMLFilter(HTMLParser, ABC):
    text = ""

    def handle_data(self, data):
        self.text += data


# Regex validate
RE_ONLY_NUMBERS = r'^(\d+)$'
RE_ONLY_CHARACTERS = r'^[a-zA-Z]+$'
RE_ONLY_NUMBER_AND_DASH = r'^[-\d]+$'
RE_ONLY_LETTERS_NUMBERS_PLUS = r'^[+A-Za-z0-9]+$'
REGEX_EMAIL = r'^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,' \
              r';:\s@\"]{2,})$'
REGEX_PHONE_NUMBER = r'^\+?[0-9]{0,20}$'
REGEX_OTP = r'[0-9]{6}'
REGEX_FULLNAME_VIETNAMESE = r"([^0-9`~!@#$%^&*(),.?'\":;{}+=|<>_\-\\\/\[\]]+)$"

REGEX_ADDRESS_VIETNAMESE = r"([^`~!@#$%^&*().?'\":;{}+=|<>_\-\\\[\]]+)$"
REGEX_VALID_PASSWORD = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?!.* ).{8,16}$'
