import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    SECRET_KEY = os.getenv("SECRET_KEY",os.urandom(16).hex())

    DB_HOST = "localhost"
    DB_NAME = "track_and_blur"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "admin"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/track_and_blur'

    UPLOAD_USER_IMG = '/static/assets/upload_usr_img'
    UPLOAD_VIDEO = '/static/assets/upload_videos'

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    SECRET_KEY = os.getenv("SECRET_KEY",os.urandom(16).hex())

    DB_HOST = "localhost"
    DB_NAME = "track_and_blur"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "admin"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/track_and_blur'

    UPLOAD_USER_IMG = '/static/assets/upload_usr_img'
    UPLOAD_VIDEO = '/static/assets/upload_videos'

    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True