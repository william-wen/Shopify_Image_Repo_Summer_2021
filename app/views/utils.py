import boto3, botocore
from flask import current_app as app
import os
from sqlalchemy.exc import IntegrityError
from app.models import db
from app.exceptions.Error import Error

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
   aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY")
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Uploads file to Amazon S3
    """
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)



def insert_db(item):
    """
    Inserts object into MySQL DB
    """
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError as e:
        status_code = e.orig.args[0]
        message = e.orig.args[1]
        raise Error(
            "Database_Error",
            message,
            status_code
        )