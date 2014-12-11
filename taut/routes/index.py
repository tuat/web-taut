from flask import Blueprint

blueprint = Blueprint('index', __name__)

@blueprint.route('/')
def index():
    return "Coming Soon"
