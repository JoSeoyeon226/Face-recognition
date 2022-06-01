from apps import db
from datetime import datetime


class Ingredient(db.Model):
    __tablename__ = 'Ingredient'

    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(64), unique=True)
    created_datetime = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return str(self.ingredient)