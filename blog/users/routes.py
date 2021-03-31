from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from blog import db
from blog.models import User, Post
from blog.users.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

users = Blueprint('users', __name__)


@users.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        password_hash = generate_password_hash(password)
        user = User(username=username,
                    email=email,
                    password_hash=password_hash)
        db.session.add(user)
        db.session.commit()

        flash("Поздравляю! Теперь вы зарегистрированный пользователь.", "success")
        return redirect(url_for('users.login'))

    return render_template('auth/registration.html', form=reg_form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = db.session.query(User) \
            .filter_by(email=login_form.email.data).first()
        if user is None or not user \
                .check_password(login_form.password.data):
            flash("Неправильное имя пользователя или пароль.", "danger")
            return redirect(url_for('users.login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template('auth/login.html', form=login_form)


@users.route('/logout', methods=['GET'])
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("Вы вышли из системы.", "success")
    return redirect(url_for('main.home'))


@users.route('/account')
@login_required
def account():
    return render_template('auth/account.html', title='Account')


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = db.session.query(Post).filter_by(author=user) \
        .order_by(Post.created.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('posts/user_posts.html', posts=posts, user=user)
