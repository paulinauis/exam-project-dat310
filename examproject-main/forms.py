# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Tittel', validators=[DataRequired()])
    body = TextAreaField('Tekst', validators=[DataRequired()])
    image = FileField('Bilde')
    tags = StringField('Kategori')
    submit = SubmitField('Publiser')
