from flask import Blueprint

blueprint = Blueprint(
    'ingredient_blueprint',
    __name__,
    url_prefix=''
)