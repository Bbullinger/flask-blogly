"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

default_pic = "https://freesvg.org/img/abstract-user-flat-4.png"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=True)
    last_name = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default=default_pic)

    posts = db.relationship("Post", backref="users")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        s = self
        return f"Class:User First Name: {s.first_name} Last Name: {s.last_name} Image URL: {s.image_url}"


class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        # datetime grabs current date and time, and turns it into a human friendly format
        db.Text,
        default=datetime.now().strftime("%Y/%M/%D, %H:%M:%S"),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"{self.poster} said {self.content} at {self.created_at}"


def connect_db(app):
    db.app = app
    db.init_app(app)
