import json
import os
from os.path import splitext
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


@image_handler.route("/upload", methods=["POST"])
@cross_origin()
def upload_file():
    uploaded_files = request.files.getlist("imgFiles[]")

    # print(request.data)
    # print(request.args)
    # print(request.form["imgFiles[]"])
    print(request.files["imgFiles[]"])
    # print(request.values)
    # print(request.json)

    added_items = []

    # uploads images to Amazon S3 Bucket
    for file in uploaded_files:
        # create the database object to prep for insertion
        img = Image(file_name=file.filename)
        print(img.id)
        insert_db(img)
        ext = splitext(img.file_name)[1]

        upload_file_to_s3(file, "{}{}".format(img.id, ext), app.config["S3_BUCKET"])

        added_items.append({
            "file_ext": ext,
            "file_name": file.filename,
            "key": img.id,
            "url": app.config["S3_LOCATION"]
        })

    return {
        "added_items": added_items
    }


@image_handler.route("/delete", methods=["DELETE"])
@cross_origin()
def delete_file():
    """
    img_id_list: List of UUIDs to delete.

    Returns uuid of the deleted keys so front end can change state and refresh.
    """
    # load req body
    img_id_list = json.loads(request.data)["img_id_list"]
    list_with_ext = []

    # delete the db entries
    for img_id in img_id_list:
        im = Image.query.filter_by(id=img_id).first()
        list_with_ext.append("{}{}".format(img_id, splitext(im.file_name)[1]))
        db.session.delete(im)
        db.session.commit()
    
    print("Image ID List", list_with_ext)
    # delete from s3
    deleted_files = delete_file_from_s3(list_with_ext, app.config["S3_BUCKET"])
    res = [splitext(key_dict["Key"])[0] for key_dict in deleted_files["Deleted"]]

    return {
        "deleted_keys": res
    }


@image_handler.route("/display", methods=["GET"])
@cross_origin()
def display_images():
    """
    Takes in nothing. Returns list of dict containing uuid and file name.
    """
    # extract all entries from 
    all_imgs = Image.query.all()
    ret = [
            {
                "key": img.id, "file_name": img.file_name, 
                "file_ext": splitext(img.file_name)[1], "url": app.config["S3_LOCATION"]
            } 
          for img in all_imgs]

    return {
        "display_list": ret
    }


@image_handler.route("/insert_db", methods=["GET"])
@cross_origin()
def test_insert():
    img = Image(file_name="hello.jpg")
    insert_db(img)
    return "hello"


@image_handler.route("/bulk_delete", methods=["GET"])
@cross_origin()
def test_delete():
    num = [1,2,3,4,5]
    Image.query.filter_by(id=1).delete()
    db.session.commit()
    return "hello"

@image_handler.route("/test", methods=["GET"])
@cross_origin()
def test():
    print(request.values)
    return "lol"