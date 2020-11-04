from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    body = TextAreaField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')