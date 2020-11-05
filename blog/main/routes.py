from flask import Blueprint
from flask import render_template, request

from blog import db
from blog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(Post).order_by(Post.created.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


@main.route('/contact')
def about():
    return render_template('contact.html', title='Контакты')