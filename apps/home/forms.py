from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class StudentListForm(FlaskForm):
    studentlist = StringField('학생목록', id='studentList', validators=[DataRequired()])
