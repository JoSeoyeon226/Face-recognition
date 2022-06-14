from flask import Blueprint

blueprint = Blueprint(
    'Capture_blueprint',
    __name__,
    url_prefix='/Capture'
)