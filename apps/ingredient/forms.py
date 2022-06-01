from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# login and registration


class IngredientForm(FlaskForm):
    ingredient = StringField('유해성분', id='ingredient', validators=[DataRequired()])
