"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

default_pic = "https://freesvg.org/img/abstract-user-flat-4.png"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=True)
    last_name = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default=default_pic)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        s = self
        return f"Class:User First Name: {s.first_name} Last Name: {s.last_name} Image URL: {s.image_url}"


def connect_db(app):
    db.app = app
    db.init_app(app)
