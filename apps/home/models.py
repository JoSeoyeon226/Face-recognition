from apps import db
from datetime import datetime


class StudentList(db.Model):
    __tablename__ = 'StudentList'

    StudentId = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(64))
    created_datetime = db.Column(db.DateTime(), unique=datetime.now())
    update_datetime = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return str(self.studentName)

