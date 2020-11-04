from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField
from wtforms.validators import InputRequired, \
    EqualTo, ValidationError, Email

from blog import db
from blog.models import User


class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('Имя пользователя', validators=[InputRequired()])
    email = StringField('Адрес электронной почты', validators=[InputRequired(), Email()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[InputRequired(),
                                                 EqualTo('password',
                                                         message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user_object = db.session.query(User).filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Имя пользователя занято. Выберите другое имя.')

    def validate_email(self, email):
        user_object = db.session.query(User).filter_by(email=email.data).first()
        if user_object:
            raise ValidationError('Адрес электронной почты занят. Пожалуйста, выбирете другой.')


class LoginForm(FlaskForm):
    """ Login form """

    email = StringField('Адрес электронной почты', validators=[InputRequired(), Email()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')