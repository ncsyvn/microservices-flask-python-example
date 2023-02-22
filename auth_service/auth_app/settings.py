import os

os_env = os.environ


class Config(object):
    SECRET_KEY = '4fF3Oi9'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProdConfig(Config):
    """Production configuration."""
    # app config
    ENV = 'prd'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    HOST = '0.0.0.0'
    TEMPLATES_AUTO_RELOAD = False

    # version
    VERSION = "1.7.0"

    # JWT Config
    JWT_SECRET_KEY = '12345678a@@@'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/auth_service'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class StgConfig(Config):
    """Staging configuration."""
    # app config
    ENV = 'stg'
    DEBUG = True
    DEBUG_TB_ENABLED = True  # Disable Debug toolbar
    TEMPLATES_AUTO_RELOAD = True
    HOST = '0.0.0.0'

    # version
    VERSION = "1.7.0"

    # JWT Config
    JWT_SECRET_KEY = '1234567a@'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    # mysql config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/auth_service'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
