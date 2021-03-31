from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
login.login_view = 'users.login'
login.login_message_category = 'info'

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from blog.models import User, Post

        db.create_all()

        from blog.users.routes import users
        from blog.posts.routes import posts
        from blog.main.routes import main
        from blog.errors.handlers import errors
        app.register_blueprint(users)
        app.register_blueprint(posts)
        app.register_blueprint(main)
        app.register_blueprint(errors)

        return app
