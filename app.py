"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "my_password"


toolbar = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()


@app.route("/")
def base():
    return redirect("/users")


@app.route("/users")
def show_all_users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/add")
def add_user_form():
    return render_template("add.html")


@app.route("/users/add", methods=["POST"])
def add_user():
    if not request.form["first_name"] or not request.form["last_name"]:
        flash("Please enter a first and last name")
        return redirect("/users/add")

    added_user = User(
        first_name=request.form["first_name"],
        last_name=request.form["last_name"],
        image_url=request.form["image_url"],
    )
    db.session.add(added_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_page(user_id):
    user = User.query.get_or_404(user_id)

    return render_template("user_page.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_get(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_post(user_id):
    User.query.get_or_404(user_id).update(
        {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "image_url": request.form["image_url"],
        }
    )
    db.session.commit()
    return render_template("users.html")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/new_post")
def add_post_get(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new_post.html", user=user)


@app.route("/users/<int:user_id>/new_post", methods=["POST"])
def add_post_post(user_id):
    if not request.form["title"] or not request.form["content"]:
        flash("Title and Content required.")
        return redirect(f"/users/{user_id}/new_post")
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form["title"], content=request.form["content"], user_id=user
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect("/users")
