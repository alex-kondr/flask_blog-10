from flask import Flask, render_template, request, redirect, url_for

from data.db.base import create_db, Session
from data.db import db_action
from data.db.models import Post


app = Flask(__name__)


@app.get("/")
def index():
    with Session() as session:
        posts = session.query(Post).all()
        return render_template("index.html", posts=posts)


@app.route("/add_post/", methods=["GET", "POST"])
def add_post():

    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        author_id = request.form.get("author_id")
        db_action.add_post(title=title, text=text, author_id=author_id)
        return redirect(url_for("index"))

    authors = db_action.get_authors()
    return render_template("add_post.html", authors=authors)


@app.route("/add_author/", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name")
        country = request.form.get("country")
        db_action.add_author(name=name, country=country)

    return render_template("add_author.html")


@app.get("/delete/post/<int:id>/")
def delete_post(id):
    db_action.del_post(id)
    return redirect(url_for("index"))


@app.route("/edit/post/<int:id>/", methods=["GET", "POST"])
def edit_post(id):
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        db_action.edit_post(id, title, text)
        return redirect(url_for("index"))

    post = db_action.get_post(id)
    return render_template("edit_post.html", post=post)


@app.get("/post/<int:id>/")
def get_post(id):
    with Session() as session:
        post = session.query(Post).where(Post.id == id).first()
        return render_template("post.html", post=post)


if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=80)
