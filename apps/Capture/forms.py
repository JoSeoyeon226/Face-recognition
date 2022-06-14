from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = StringField("file", validators=[DataRequired()])
    name = StringField("name")