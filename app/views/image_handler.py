import json
import os
import shutil
from flask import Blueprint, request, render_template
from flask import current_app as app
from flask_cors import cross_origin
from app.models import db, Image
from app.views.utils import (
    upload_file_to_s3,
    insert_db
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
    print(uploaded_files)

    # uploads images to Amazon S3 Bucket
    for file in uploaded_files:
        link = upload_file_to_s3(file, app.config["S3_BUCKET"])

    # uploads

    return "hello"