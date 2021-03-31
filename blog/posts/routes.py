from flask import (Blueprint, render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваша статья была создана!', 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/create_post.html', title='Создать новую статью',
                           form=form, legend='Создать новую статью')


@posts.route("/post/<slug>")
def post(slug):
    post = db.session.query(Post).filter(Post.slug == slug).first()
    return render_template('posts/post.html', title=post.title, post=post)


@posts.route("/post/<slug>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = db.session.query(Post).filter(Post.slug == slug).first()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Ваша статья была отредактирована!', 'success')
        return redirect(url_for('posts.post', slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('posts/create_post.html', title='Редактировать статью',
                           form=form, legend='Редактировать статью')


@posts.route("/post/<slug>/delete", methods=['POST'])
@login_required
def delete_post(slug):
    post = db.session.query(Post).filter(Post.slug == slug).first()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваша статья была удалена!', 'success')
    return redirect(url_for('main.home'))
