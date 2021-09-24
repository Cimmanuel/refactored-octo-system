import os

from flask import Flask

from .accounts import accounts
from .bookmarks import bookmarks
from .database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if not test_config:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    app.register_blueprint(accounts)
    app.register_blueprint(bookmarks)

    return app
