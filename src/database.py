import secrets
import string
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

RANDOM_STRING_CHARS = string.ascii_letters + string.digits


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    bookmarks = db.relationship("Bookmark", backref="user")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return f"{self.username}'s account"


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.SmallInteger, db.ForeignKey("user.id"))
    description = db.Column(db.Text(), nullable=True)
    url = db.Column(db.Text(), nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.SmallInteger, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.get_random_string()

    def get_random_string(
        self, length=3, allowed_characters=RANDOM_STRING_CHARS
    ):
        characters = "".join(
            secrets.choice(allowed_characters) for i in range(length)
        )
        link = self.query.filter_by(short_url=characters).first()

        if link:
            self.get_random_string()
        else:
            return characters

    def __repr__(self):
        return f"{self.short_url}"
