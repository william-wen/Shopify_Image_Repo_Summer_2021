import os

class Config:
    # Flasks Configuration Variables
    # SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = "development"
    FLASK_APP = "app"
    FLASK_DEBUG = 1

    # Amazon S3 File Storage Variables
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    # DB Info
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    HOST = os.environ.get("DB_HOST_NAME")
    DB_PORT = os.environ.get("DB_PORT")
    SCHEMA_NAME = os.environ.get("SCHEMA_NAME")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        DB_USERNAME, DB_PASSWORD, HOST, DB_PORT, SCHEMA_NAME
    )
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debugging Info
    SECRET_KEY = os.urandom(32)
    DEBUG = True
    PORT = 5000