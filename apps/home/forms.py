from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class FileForm(FlaskForm):
    file = StringField("file", validators=[DataRequired()])
    name = StringField("name")
    number = StringField("number")
    subject = StringField("subject")


class SubjectForm(FlaskForm):
    professor = StringField("professor")
    subject_name = StringField("subject_name")
    subject_code = StringField("subject_code", validators=[DataRequired()])
    semester = StringField("semester")
