from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        title = request.form.get("title")
        if not text:
            flash("Post cannot be empty", category="danger")
        elif not title:
            flash("Title cannot be empty!", category="danger")
        else:
            post = Post(title=title, text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            
            flash("Post created!", category="success") 
            return redirect(url_for("views.home"))
            


    return render_template("createpost.html", user=current_user)

# deleteing the post that is created by the user.
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist." , category="danger")
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post!", category="danger")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post successfully deleted!", category="success")

    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists!", category="danger")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template('posts.html', user=current_user, posts=posts, username=username)