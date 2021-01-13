import json
import os
import shutil
from flask import Blueprint, request, render_template
from flask import current_app as app
from flask_cors import cross_origin
from app.models import db, Image
from app.views.utils import (
    insert_db,
    delete_file_from_s3,
    get_files,
    upload_file_to_s3
)

image_handler = Blueprint("image_handler", __name__)

@image_handler.route("/")
@cross_origin()
def index():
    return render_template("index.html")

@image_handler.route("/", methods=["POST"])
@cross_origin()
def upload_file():
    uploaded_files = request.files.getlist("hello_file")

    # uploads images to Amazon S3 Bucket
    for file in uploaded_files:
        link = upload_file_to_s3(file, app.config["S3_BUCKET"])

    return "success"

@image_handler.route("/delete", methods=["DELETE"])
@cross_origin()
def delete_file():
    # extract links from the db
    test = ["test1.jpg", "test2.jpg"]
    res = delete_file_from_s3(test, app.config["S3_BUCKET"])
    # delete
    return "hello"

@image_handler.route("/display", methods=["GET"])
@cross_origin()
def display_images():
    objects = get_files(app.config["S3_BUCKET"])
    print(objects)
    print(type(objects))
    keys = [el["Key"] for el in objects["Contents"]]

    return {
        "keys": keys
    }