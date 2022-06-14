# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()

upload_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

fonts_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "fonts")
if not os.path.exists(fonts_dir):
    os.makedirs(fonts_dir)

models_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "models")
face_names_dir = os.path.join(upload_dir, "face_names")
custom_face_model_dir = os.path.join(models_dir, "custom_face_model")


# face_images_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "face_images")


def allowed_image_file(filename):
    allowed_extensions = ["png", "jpg", "jpeg", "gif"]
    return "." in filename and \
           filename.rsplit(".", 1)[1] in allowed_extensions


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):

    for module_name in ('authentication', 'home', 'Capture'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)

    from flask_socketio import SocketIO
    socketio = SocketIO()
    socketio.init_app(app)

    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

