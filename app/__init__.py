from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app.exceptions.Error import Error
import os
from dotenv import load_dotenv

db  = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="../build", static_url_path="/")

    # load env variables in if they aren't auto-loaded
    load_dotenv()

    app.config.from_object("config.Config")

    db.init_app(app)

    # import all the blueprints
    from app.views.image_handler import image_handler
    app.register_blueprint(image_handler)

    # error handler
    app.register_error_handler(Error, handle_error)

    with app.app_context():
        db.create_all()

    return app

def handle_error(e):
    response = e.to_dict()
    return response